from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Group, User, CheckList, user_group


# ㅁㄴㅇㅁㅇ

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

# ㄴㅁㅇㅁㅇ


from urllib.parse import quote_plus


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


password = 'alalwl123!@#'
encoded_password = quote_plus(password)

engine = create_engine(f'mysql+pymysql://root:{encoded_password}@localhost/sprog')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    description = StringField('자기소개', validators=[DataRequired()])
    submit = SubmitField('회원가입')

class GroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    group_info = TextAreaField('Group Info', validators=[DataRequired()])
    submit = SubmitField('Edit Group')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homeList'))

    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(name=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('homeList'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(name=form.username.data).first()
        if user:
            return '유저 이름이 이미 존재합니다.'
            # return redirect(url_for('register'))

        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data)  # 비밀번호 해시화하여 설정
        new_user.set_description(form.description.data) # 개인소개 설정
        session.add(new_user)
        session.commit()
        flash('회원가입이 성공적으로 완료되었습니다.')

        return redirect(url_for('login'))

    return render_template('sign-up.html', title='Register', form=form)

@app.route('/groups/<int:group_id>/list')
def groupList(group_id=None):
    group = session.query(Group).filter_by(id=group_id).one()
    users = session.query(user_group).filter_by(group_id=group_id)
    checklist = session.query(CheckList).filter_by(group_id=group_id)
    return render_template(
        'group-details.html', group=group, current_user = current_user, user=users, checklist=checklist)

@app.route('/groups/<int:group_id>')
def groupDetail(group_id=None):
    group = session.query(Group).filter_by(id=group_id).one()
    user_ids = [user.user_id for user in session.query(user_group).filter_by(group_id=group_id).all()]
    users = session.query(User).filter(Group.id.in_(user_ids)).all()
    checklist = session.query(CheckList).filter_by(group_id=group_id)
    print(checklist)
    return render_template(
        'scheduler.html', group=group, user=users, checklist=checklist,current_user = current_user)



@app.route('/groups/<int:group_id>/<int:user_id>/new', methods=['POST'])
def newGroupMem(group_id=None,user_id=None):
    group = session.query(Group).filter_by(id=group_id).one()
    user = session.query(User).filter_by(id=user_id).one()

    session.add(user)
    session.add(group)
    session.commit()

    if group not in user.groups:
        user.groups.append(group)
        session.commit()
    else:
        return '이미 가입된 유저입니다.'

    return redirect(url_for('homeList'))

@app.route('/groups/<int:group_id>/<int:user_id>/remove', methods=['POST'])
def groupMemDelete(group_id=None,user_id=None):
    group = session.query(Group).filter_by(id=group_id).one()
    user = session.query(User).filter_by(id=user_id).one()

    if group in user.groups:
        user.groups.remove(group)
        session.commit()
    else :
        return '이미 없는 유저입니다.'
    return redirect(url_for('homeList'))

@app.route('/groups/new', methods=['GET', 'POST'])
def newGroup():
    if request.method == 'POST':
        newGroup = Group(name=request.form['group-name'],description=request.form['group-info'])
        session.add(newGroup)
        session.commit()
        tasks = request.form.getlist('task[]')

        for task_content in tasks:
            checkList = CheckList(content=task_content, group_id=newGroup.id,completed=False)
            session.add(checkList)

        session.commit()  # 모든 Task 객체 저장
        return redirect(url_for('homeList'))
    else:
        return render_template('schedule-registration.html')


@app.route('/groups/<int:group_id>/edit',
           methods=['GET', 'POST'])
def editGroup(group_id):
    editedGroup = session.query(Group).filter_by(id=group_id).one()
    editedTasks = session.query(CheckList).filter_by(group_id=group_id).all()
    print(editedTasks)



    if request.method == 'POST':
        if request.form['group-name']:
            editedGroup.name = request.form['group-name']
        if request.form['group-info']:
            editedGroup.description = request.form['group-info']

        tasks = request.form.getlist('task[]')
        completed = request.form.getlist('completed[]')

        for task, task_content, is_completed in zip(editedTasks, tasks, completed):
            checklist = session.query(CheckList).filter_by(id=task.id).one()
            checklist.content = task_content
            is_completed = True if is_completed == 'on' else False
            checklist.completed = is_completed
            session.add(checklist)
        session.commit()


        return redirect(url_for('groupList', group_id=group_id))
    else:
        return render_template(
            'editgroup.html', group_id=group_id, group=editedGroup, checklist=editedTasks)




@app.route('/')
def homeList():
    group = session.query(Group).all()
    return render_template(
        'home.html', group=group, current_user = current_user)


@app.route('/groups/<int:group_id>/<int:checklist_id>/delete',
           methods=['POST'])
def deleteCheckList(group_id, checklist_id):
    checklist = session.query(CheckList).filter_by(id=checklist_id).one()
    session.delete(checklist)
    session.commit()
    print('확인!!')
    return redirect(url_for('homeList'))


@app.route('/user/<int:user_id>')
def userProfile(user_id=None):
    user = session.query(User).filter_by(id=user_id).one()

    group_ids = [group.group_id for group in session.query(user_group).filter_by(user_id=user_id).all()]
    groups = session.query(Group).filter(Group.id.in_(group_ids)).all()
    return render_template(
        'profile.html', user=user, groups = groups)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
