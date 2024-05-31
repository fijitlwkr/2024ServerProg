import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine, text

from urllib.parse import quote_plus

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'password' : self.password,
            'groups': [group.serialize for group in self.groups]
        }


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    # bookstore_id = Column(Integer, ForeignKey('bookstore.id'))
    # bookstore = relationship(BookStore)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'users': [user.serialize for user in self.users]
        }

# User와 Group 사이의 중간 테이블 정의
user_group_table = Table('user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True)
)

class CheckList(Base):
    __tablename__ = 'checklist'

    id = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship(Group)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'content': self.name,
            'id': self.id,
            'completed' : self.password
        }



password = 'alalwl123!@#'
encoded_password = quote_plus(password)




# 엔진 생성
engine = create_engine(f'mysql+pymysql://root:{encoded_password}@localhost/')

# 데이터베이스 생성 SQL 명령문 실행
with engine.connect() as connection:
    connection.execute(text("CREATE DATABASE sprog DEFAULT CHARACTER SET UTF8;"))
    print("Database 'sprog' created successfully.")


# f-string을 사용하여 데이터베이스 연결 문자열 생성
engine = create_engine(f'mysql+pymysql://root:{encoded_password}@localhost/sprog')

Base.metadata.create_all(engine)
