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
    common_id=db.Column(db.Integer,primary_key=True)
    common_name=db.Column(db.String(32),unique=True,nullable=False)
    common_password = db.Column(db.String(255),nullable=False)
    # user_type = db.Column(db.String(10))


class senior_user(db.Model):#senior user is in charge of the restaurant
    __tablename__="senior_user"
    senior_id=db.Column(db.Integer,primary_key=True)
    senior_name=db.Column(db.String(32),unique=True,nullable=False)
    res_id=db.Column(db.Integer, db.ForeignKey('namelist.list_id'))

class restaurants(db.Model):
    __tablename__="restaurants"
    restaurant_id = db.Column(db.Integer,primary_key=True)
    restaurant_name = db.Column(db.String(32),unique=True,nullable=False)
    location = db.Column(db.String(64),unique=True,nullable=False)
    open_hour = db.Column(db.String(64),unique=True,nullable=False)
    meal_type = db.Column(db.String(64),unique=True,nullable=False)
    average_price_per_person = db.Column(db.Float,primary_key=True)
    rate = db.Column(db.Float,primary_key=True)

class dishes(db.Model):
    __tablename__="dishes"
    list_id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(40), primary_key=True)
    info_type = db.Column(db.String(16))
    info_price = db.Column(db.Integer)
    info_taste = db.Column(db.String(16))
    info_times = db.Column(db.Integer)

#needs further adjustment:other link for senior user to login
@app.route('/', methods=['GET', 'POST'])
def common_register():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        check1=common_user.query.all()#read from common user
        checka=0
        checkb=0
        for i in check1:
            if i.common_name==username:#check whether the user exists
                checka=1
                if i.common_password==password:
                    checkb=1
                else:
                    checkb=0
            else:
                checka=0
            if checka==1:
                break
        if checka != 1:
            flash(u'the account does not exist!')
        elif checkb != 1:
            flash(u"wrong password or user name!")
        else:
            return redirect(url_for('info'))
    return render_template("login.html")


@app.route('/senior_register', methods=['GET', 'POST'])
def senior_register():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        check1=senior_user.query.all()#read from common user
        checka=0
        checkb=0
        for i in check1:
            if i.senior_name==username:#check whether the user exists
                checka=1
                if i.senior_password==password:
                    checkb=1
                else:
                    checkb=0
            else:
                checka=0
            if checka==1:
                break
        if checka != 1:
            flash(u'the account does not exist!')
        elif checkb != 1:
            flash(u"wrong password or user name!")
        else:
            #needs modification: leads to the users' corresponding restaurant
            return redirect(url_for('info'))
    #this line may be modified to return render_template("senior_login.html")
    return render_template("login.html")

# push test











