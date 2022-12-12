from flask import Flask, render_template, request, flash, url_for, redirect#request是一个请求对象
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:password@127.0.0.1/flaskproj3'
app.secret_key='bilibili'




