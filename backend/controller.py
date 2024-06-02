from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Group, User, CheckList, user_group

from urllib.parse import quote_plus


app = Flask(__name__)



password = 'temp'
encoded_password = quote_plus(password)

engine = create_engine(f'mysql+pymysql://root:{encoded_password}@localhost/sprog')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/groups/<int:group_id>/list')
def groupList(group_id=None):
    group = session.query(Group).filter_by(id=group_id).one()
    users = session.query(user_group).filter_by(group_id=group_id)
    checklist = session.query(CheckList).filter_by(group_id=group_id)
    return render_template(
        'group-details.html', group=group, user=users, checklist=checklist)

@app.route('/groups/<int:group_id>')
def groupDetail(group_id=None):
    group = session.query(Group).filter_by(id=group_id).one()
    user_ids = [user.user_id for user in session.query(user_group).filter_by(group_id=group_id).all()]
    users = session.query(User).filter(Group.id.in_(user_ids)).all()
    checklist = session.query(CheckList).filter_by(group_id=group_id)
    print(checklist)
    return render_template(
        'scheduler.html', group=group, user=users, checklist=checklist)



@app.route('/groups/<int:group_id>/<int:user_id>/new', methods=['POST'])
def newGroupMem(group_id=None,user_id=None):
    group = session.query(Group).filter_by(id=group_id).one()
    user = session.query(User).filter_by(id=user_id).one()

    session.add(user)
    session.add(group)
    session.commit()

    # Associate the user with the group
    user.groups.append(group)

    # Commit the session to save the association
    session.commit()

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
        'home.html', group=group)


@app.route('/restaurants/<int:group_id>/<int:checklist_id>/delete',
           methods=['POST'])
def deleteCheckList(group_id, checklist_id):
    checklist = session.query(CheckList).filter_by(id=checklist_id).one()
    session.delete(checklist)
    session.commit()
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
