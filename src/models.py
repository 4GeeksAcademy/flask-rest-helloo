import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    posts = relationship('Post', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', backref='followed', lazy=True)
    following = relationship('Follower', foreign_keys='Follower.user_from_id', backref='follower', lazy=True)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_url = Column(String(255))
    caption = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)

    comments = relationship('Comment', backref='post', lazy=True)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)

# Diagrama ER automático
def generate_er_diagram():
    try:
        render_er(Base, 'diagram.png')
        print("✅ Diagrama generado correctamente: diagram.png")
    except Exception as e:
        print("❌ Hubo un problema generando el diagrama")
        raise e

# Ejecutar si es el script principal
if __name__ == '__main__':
    generate_er_diagram()
