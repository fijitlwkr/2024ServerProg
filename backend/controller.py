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
def groupList(bookstore_id=None, group_id=None):
    group = session.query(Group).filter_by(id=group_id).one()
    users = session.query(user_group).filter_by(group_id=group_id)
    checklist = session.query(CheckList).filter_by(group_id=group_id)
    return render_template(
        'group-details.html', group=group, user=users, checklist=checklist)


@app.route('/groups/<int:group_id>/new', methods=['GET', 'POST'])
def newGroupMem(bookstore_id):

    return 0

@app.route('/groups/new', methods=['GET', 'POST'])
def newGroup():
    if request.method == 'POST':
        newGroup = Group(name=request.form['group-name'],description=request.form['group-info'])
        print(newGroup)
        session.add(newGroup)
        session.commit()
        return redirect(url_for('groupList', group_id=1))
    else:
        return render_template('schedule-registration.html')

@app.route('/')
def homeList():
    group = session.query(Group).all()
    return render_template(
        'home.html', group=group)


@app.route('/user/<int:user_id>')
def userProfile():
    return 0

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
