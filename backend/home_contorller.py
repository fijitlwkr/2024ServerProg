from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Group, User, CheckList, user_group

from urllib.parse import quote_plus


app = Flask(__name__)



password = 'alalwl123!@#'
encoded_password = quote_plus(password)

engine = create_engine(f'mysql+pymysql://root:{encoded_password}@localhost/sprog')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def homeList():
    group = session.query(Group).all()
    return render_template(
        'home.html', group=group)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)

