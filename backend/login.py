from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = '수정 필요'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  #수정 필요

#Flask-login 초기화
db = SQLAlchemy(app) 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 사용자 모델 정의
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)


# 사용자 로드 함수
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 로그인 폼
class LoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

# 회원가입 폼
class RegistrationForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('회원가입')

#로그인 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data): # 제출 후 로그인 처리
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('아이디 또는 비밀번호가 일치하지 않습니다.')
    return render_template('login.html', title='Login', form=form)

#회원가입 라우트
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():    
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('유저 이름이 이미 존재합니다.')
            return redirect(url_for('register'))
        
        new_user = User(username=form.username.data)
        db.session.add(new_user)
        db.session.commit()
        flash('회원가입이 성공적으로 완료되었습니다.')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

#로그아웃 라우트
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html', title='Home')

#홈 화면 접근 정의
@app.route('/protected')
@login_required
def protected():
    return '제한된 접근입니다.'

# 로컬 환경 실행 - 변경 필요
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)