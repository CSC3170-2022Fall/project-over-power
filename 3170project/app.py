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
    info_type = db.Column(db.String(16),unique=False,nullable=False)
    info_price = db.Column(db.Integer,unique=False,nullable=False)
    info_taste = db.Column(db.String(16),unique=False,nullable=False)
    info_times = db.Column(db.Integer,unique=False,nullable=False)

class rate(db.Model):
    __tablename__="rate"
    restaurant_id = db.Column(db.Integer, primary_key=True)
    environment_rate = db.Column(db.Float(1), nullable=True)
    service_rate = db.Column(db.Float(1), nullable=True)
    taste_rate = db.Column(db.Float(1), nullable=True)
    price_rate = db.Column(db.Float(1), nullable=True)
    overall_rate = db.Column(db.Float(1), nullable=True)

class comment(db.Model):
    __tablename__ = "comment"
    restaurant_id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(32), primary_key=True)
    common_id = db.Column(db.Integer, primary_key=True)
    Comment_Time = db.Column(db.String(48), unique=True, nullable=False)#using the system time, you should import "datetime" and "time"
    content = db.Column(db.String(500))#free edit

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
    return render_template("normal_login.html")

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
    return render_template("senior_login.html")

@app.route('/create account', methods=['GET', 'POST'])
def user_create():
    if request.method=="POST":
        username=request.form.get('username')
        pw=request.form.get('password')
        pw2=request.form.get('password2')
        check7=common_user.query.filter_by(user_name=username).first()#筛选filter_by，检测table1中是否已存在该用户名
        if check7:
            flash('User already exist!')
        else:
            if len(username)!=0:
                if pw==pw2 and len(pw)!=0:
                    user=common_user(user_name=username, user_password=pw)
                    db.session.add_all([user])
                    db.session.commit()
                    flash('Creating an account succeeded, you can log in with this account now!')
                else:
                    flash('Password confirmation failed!')
            else:
                flash('Please enter the user name')
    return render_template('create_account.html')

@app.route('/info', methods=['GET', 'POST'])
def main():#餐厅系统主界面（餐厅列表页）
    a1=restaurants.query.all()
    return render_template('info.html',a1=a1)#主页面为info.html，传入参数a1(restaurant列表)



if __name__ == '__main__':
    app.run()
