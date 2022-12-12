from flask import Flask, render_template, request, flash, url_for, redirect#request是一个请求对象
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:password@127.0.0.1/flaskproj3'
app.secret_key='bilibili'

class common_user(db.Model):#datapage model, inherited from db.Model
    #define the table name
    __tablename__="common_users"
    #define the content
    user_id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(32),unique=True,nullable=False)
    user_password = db.Column(db.String(255),nullable=False)
    # user_type = db.Column(db.String(10))

# class senior_user(db.Model):
#      __tablename__="senior_users"
#     #define the content
#     user_id=db.Column(db.Integer,primary_key=True)
#     user_name=db.Column(db.String(32),unique=True,nullable=False)
#     user_password = db.Column(db.String(255),nullable=False)



