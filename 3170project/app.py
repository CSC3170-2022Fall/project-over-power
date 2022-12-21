from flask import Flask, render_template, request, flash, url_for, redirect#request是一个请求对象
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:password@127.0.0.1/3170project'
app.secret_key='bilibili'

class common_user(db.Model):#datapage model, inherited from db.Model
    #define the table name
    __tablename__="common_user"
    #define the content
    common_id=db.Column(db.Integer,primary_key=True)
    common_name=db.Column(db.String(32),unique=True,nullable=False)
    common_password = db.Column(db.String(255),nullable=False)
    # user_type = db.Column(db.String(10))


class senior_user(db.Model):#senior user is in charge of the restaurant
    __tablename__="senior_user"
    senior_id=db.Column(db.Integer,primary_key=True)
    senior_name=db.Column(db.String(32),unique=True,nullable=False)
    res_id=db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))

class restaurants(db.Model):
    __tablename__="restaurants"
    restaurant_id = db.Column(db.Integer,primary_key=True)
    restaurant_name = db.Column(db.String(32),unique=True,nullable=False)
    location = db.Column(db.String(64),unique=True,nullable=False)
    open_hour = db.Column(db.String(64),unique=True,nullable=False)
    meal_type = db.Column(db.String(64),unique=True,nullable=False)
    average_price_per_person = db.Column(db.Float,primary_key=True)
    rate = db.Column(db.Float,primary_key=True)

# class dishes(db.Model):
#     __tablename__="dishes"
#     list_id = db.Column(db.Integer, primary_key=True)
#     list_name = db.Column(db.String(40), primary_key=True)
#     info_type = db.Column(db.String(16),unique=False,nullable=False)
#     info_price = db.Column(db.Integer,unique=False,nullable=False)
#     info_taste = db.Column(db.String(16),unique=False,nullable=False)
#     info_times = db.Column(db.Integer,unique=False,nullable=False)

class dishes(db.Model):
    __tablename__ = "dishes"
    list_id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(40),unique=False, nullable=False)
    info_type = db.Column(db.String(16), unique=False, nullable=False)
    info_price = db.Column(db.Integer, unique=False, nullable=False)
    info_taste_M = db.Column(db.Integer, unique=False, nullable=False)
    info_taste_N = db.Column(db.Integer, unique=False, nullable=False)
    info_taste_X = db.Column(db.Integer, unique=False, nullable=False)
    info_taste_Y = db.Column(db.Integer, unique=False, nullable=False)
    info_taste_Z = db.Column(db.Integer, unique=False, nullable=False)
    info_times = db.Column(db.Integer, unique=False, nullable=False)
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurants.restaurant_id'))

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
    common_id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer,db.ForeignKey(dishes.list_id))
    Comment_Time = db.Column(db.String(48), unique=True, nullable=False)#using the system time, you should import "datetime" and "time"
    content = db.Column(db.String(500))#free edit
    
class login_user(db.Model):#record the id of the user
    _tablename_="login_user"
    info=db.Column(db.Integer,primary_key=True)
    
# class preference(db.Model):
#     _tablename_="preference"
#     common_id=db.Column(db.Integer,primary_key=True)
#     A_dish_type=db.Column(db.Integer, nullable=True)
#     B_dish_type = db.Column(db.Integer, nullable=True)
#     C_dish_type = db.Column(db.Integer, nullable=True)
#     D_dish_type = db.Column(db.Integer, nullable=True)
#     M_dish_taste = db.Column(db.Integer, nullable=True)
#     N_dish_taste = db.Column(db.Integer, nullable=True)
#     X_dish_taste = db.Column(db.Integer, nullable=True)
#     Y_dish_taste = db.Column(db.Integer, nullable=True)
#     Z_dish_taste = db.Column(db.Integer, nullable=True)

class preference(db.Model):
    _tablename_="preference"
    common_id=db.Column(db.Integer,primary_key=True)
    A_type=db.Column(db.Integer, nullable=True)
    B_type = db.Column(db.Integer, nullable=True)
    C_type = db.Column(db.Integer, nullable=True)
    D_type = db.Column(db.Integer, nullable=True)
    M_taste = db.Column(db.Integer, nullable=True)
    N_taste = db.Column(db.Integer, nullable=True)
    X_taste = db.Column(db.Integer, nullable=True)
    Y_taste = db.Column(db.Integer, nullable=True)
    Z_taste = db.Column(db.Integer, nullable=True)
    
@app.route("/preference_record",methods=["GET","POST"])
def preference_record():
    if request.method=="POST":
        user_id = db.session.execute("select info from login_user")#get user'sid
        A_dish_type = request.form.get("A_dish_type")#get user's dish type
        B_dish_type = request.form.get("B_dish_type")
        C_dish_type = request.form.get("C_dish_type")
        D_dish_type = request.form.get("D_dish_type")
        M_dish_taste = request.form.get("M_dish_type")#get user's taste
        N_dish_taste = request.form.get("N_dish_type")
        X_dish_taste = request.form.get("X_dish_type")
        Y_dish_taste = request.form.get("Y_dish_type")
        Z_dish_taste = request.form.get("Z_dish_type")
        www=preference(common_id=user_id,A_type=A_dish_type,B_type=B_dish_type,C_type=C_dish_type,D_type=D_dish_type,M_taste=M_dish_taste,N_taste=N_dish_taste,X_taste=X_dish_taste,Y_taste=Y_dish_taste,Z_taste=Z_dish_taste)
        db.session.add_all([www])
        db.session.commit()
        return redirect(url_for("main"))
    # return redirect(url_for("preference"))
    return render_template("preference.html")


# @app.route("/preference/",methods=["GET","POST"])
# def preference_record():
#     if request.method=="POST":
#         user_id = common_("user_id")#获取用户id
#         A_dish_type=request.form.get("A_dish_type")#获取用户dish type
#         B_dish_type = request.form.get("B_dish_type")
#         C_dish_type = request.form.get("C_dish_type")
#         D_dish_type = request.form.get("D_dish_type")
#         M_dish_taste = request.form.get("M_dish_type")#获取用户taste
#         N_dish_taste = request.form.get("N_dish_type")
#         X_dish_taste = request.form.get("X_dish_type")
#         Y_dish_taste = request.form.get("Y_dish_type")
#         Z_dish_taste = request.form.get("Z_dish_type")

@app.route("/edit_preference_record",methods=["GET","POST"])
def edit_preference_record():
    if request.method=="POST":
        user_id = db.session.execute("select info from login_user")#get user's id
        aim_info = preference.query.get(user_id)#delete the initial information of user's preference
        db.session.delete(aim_info)
        db.session.commit()
        A_dish_type = request.form.get("A_dish_type")#获取用户dish type
        B_dish_type = request.form.get("B_dish_type")
        C_dish_type = request.form.get("C_dish_type")
        D_dish_type = request.form.get("D_dish_type")
        M_dish_taste = request.form.get("M_dish_type")#获取用户taste
        N_dish_taste = request.form.get("N_dish_type")
        X_dish_taste = request.form.get("X_dish_type")
        Y_dish_taste = request.form.get("Y_dish_type")
        Z_dish_taste = request.form.get("Z_dish_type")
        www=preference(common_id=user_id,A_type=A_dish_type,B_type=B_dish_type,C_type=C_dish_type,D_type=D_dish_type,M_taste=M_dish_taste,N_taste=N_dish_taste,X_taste=X_dish_taste,Y_taste=Y_dish_taste,Z_taste=Z_dish_taste)
        db.session.add_all([www])#re-add the info
        db.session.commit()
    return redirect(url_for("preference"))

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
            print(username)
            print(i.common_name)
            if i.common_name==username:#check whether the user exists
                checka=1
                get_id = i.common_id
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
            # get_id = db.session.execute("select common_id from flaskproject3.common_user where common_name=username").fetchone()
            qqq = login_user(info=get_id)
            db.session.add_all([qqq])
            db.session.commit()#this should be added to all the common user login after using the username
            return redirect(url_for('main'))

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
            return redirect(url_for("preference_record"))
    #this line may be modified to return render_template("senior_login.html")
    return render_template("senior_login.html")

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method=="POST":
        username=request.form.get('username')
        pw=request.form.get('password')
        pw2=request.form.get('password2')
        check7=common_user.query.filter_by(common_name=username).first()#筛选filter_by，检测table1中是否已存在该用户名
        if check7:
            flash('User already exist!')
        else:
            if len(username)!=0:
                if pw==pw2 and len(pw)!=0:
                    user=common_user(common_name=username, common_password=pw)
                    db.session.add_all([user])
                    db.session.commit()
                    flash('Creating an account succeeded, you can log in with this account now!')
                    # return render_template('preference.html')
                    return redirect(url_for("preference_record"))
                else:
                    flash('Password confirmation failed!')
            else:
                flash('Please enter the user name')
    return render_template('create_account.html')

@app.route('/main', methods=['GET', 'POST'])
def main():#餐厅系统主界面（餐厅列表页）
    a1=restaurants.query.all()
    return render_template('info.html',a1=a1)#主页面为info.html，传入参数a1(restaurant列表)
    
def search():
    content = request.form.get('content') 
    if content is None:
        content = " "
    dish_name = dishes.query.filter(dishes.list_name.like("%"+content+"%")if content is not None else "").all() 
    return render_template('search.html',quotes = dish_name)

db.drop_all()
db.create_all()
#为table加入数据
user1=common_user(common_name='zzz', common_password='12345')
user2=common_user(common_name='qqq', common_password='16949')
db.session.add_all([user1, user2])
db.session.commit()

if __name__ == '__main__':
    app.run()

