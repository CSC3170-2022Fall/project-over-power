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
    common_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    common_name=db.Column(db.String(32),unique=True,nullable=False)
    common_password = db.Column(db.String(255),nullable=False)
    # user_type = db.Column(db.String(10))


class senior_user(db.Model):#senior user is in charge of the restaurant
    __tablename__="senior_user"
    senior_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    senior_name=db.Column(db.String(32),unique=True,nullable=False)
    res_id=db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))
    senior_password = db.Column(db.String(255),nullable=False)

class restaurants(db.Model):
    __tablename__="restaurants"
    restaurant_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
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
    list_id = db.Column(db.String(10), primary_key=True)#已修改
    list_name = db.Column(db.String(40),unique=False, nullable=True)
    info_type = db.Column(db.String(16), unique=False, nullable=True)
    info_description = db.Column(db.String(16),unique=False,nullable=True)
    info_price = db.Column(db.Integer, unique=False, nullable=True)
    info_taste_M = db.Column(db.Integer, unique=False, nullable=True)
    info_taste_N = db.Column(db.Integer, unique=False, nullable=True)
    info_taste_X = db.Column(db.Integer, unique=False, nullable=True)
    info_taste_Y = db.Column(db.Integer, unique=False, nullable=True)
    info_taste_Z = db.Column(db.Integer, unique=False, nullable=True)
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurants.restaurant_id'))

class rate(db.Model):
    __tablename__="rate"
    restaurant_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    environment_rate = db.Column(db.Float(1), nullable=True)
    service_rate = db.Column(db.Float(1), nullable=True)
    taste_rate = db.Column(db.Float(1), nullable=True)
    price_rate = db.Column(db.Float(1), nullable=True)
    overall_rate = db.Column(db.Float(1), nullable=True)

class comment(db.Model):
    __tablename__ = "comment"
    comment_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    dish_id = db.Column(db.String(10),db.ForeignKey(dishes.list_id))
    Comment_Time = db.Column(db.String(48), unique=True, nullable=False)#using the system time, you should import "datetime" and "time"
    content = db.Column(db.String(500))#free edit
    
class login_user(db.Model):#record the id of the user
    _tablename_="login_user"
    login_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    login_info=db.Column(db.Integer,nullable=False)
 
class current_dish(db.Model):#record the current dish that the user is viewing
    _tablename_="login_user"
    login_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    login_info=db.Column(db.Integer,nullable=False)
    
class preference(db.Model):
    _tablename_="preference"
    common_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    A_type=db.Column(db.Integer, nullable=True)
    B_type = db.Column(db.Integer, nullable=True)
    C_type = db.Column(db.Integer, nullable=True)
    D_type = db.Column(db.Integer, nullable=True)
    M_taste = db.Column(db.Integer, nullable=True)
    N_taste = db.Column(db.Integer, nullable=True)
    X_taste = db.Column(db.Integer, nullable=True)
    Y_taste = db.Column(db.Integer, nullable=True)
    Z_taste = db.Column(db.Integer, nullable=True)    
    
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
    
@app.route("/preference_record",methods=["GET","POST"])
def preference_record():
    if request.method=="POST":
        temp=request.values.get("button1")
        temp2=request.values.get("button2")
        if (temp2=="Back"):
            return redirect(url_for("common_register")) 
        else:
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
        temp=request.values.get("button1")
        temp2=request.values.get("button2")
        if (temp2=="Back"):
            return redirect(url_for("main")) 
        else:
            user_id = db.session.execute("select info from login_user")#get user'sid
            check=preference.query.get(user_id)
            db.session.delete(check)
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
    return render_template("edit_preference.html")

#needs further adjustment:other link for senior user to login
@app.route('/', methods=['GET', 'POST'])
def common_register():
    check_login=login_user.query.all()
    for i in check_login:
        if i.login_info!='':
            temp=login_user(i.login_id)
            login_user.delete(temp)
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
            qqq = login_user(login_info=get_id)
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
            # return redirect(url_for(""))
            return render_template('resta_1.html') 
    #this line may be modified to return render_template("senior_login.html")
    return render_template("senior_login.html")

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    check_login=login_user.query.all()
    for i in check_login:
        if i.login_info!='':
            temp=login_user(i.login_id)
            login_user.delete(temp)
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

# @app.route("/resta_1",methods=["GET","POST"])
# def resta_1():
#     if request.method=="GET":
#         dish_table = dishes.query.filter_by(restaurant_id=1).all()
#     return render_template("?resta_1.html",dish_table=dish_table) 


# def search():
#     content = request.form.get('content') 
#     if content is None:
#         content = " "
#     dish_name = dishes.query.filter(dishes.list_name.like("%"+content+"%")if content is not None else "").all() 
#     return render_template('search.html',quotes = dish_name)

@app.route('/main', methods=['GET', 'POST'])
def main():#餐厅系统主界面（餐厅列表页）
    if request.method=="GET":
        user = login_user.query.all()
        user_id=user.login_info
        #user_id = login_user(info=get_id)  # get useflr's id
        user_info = preference.query.get(user_id)
        user_taste_M = user_info.M_taste
        user_taste_N = user_info.N_taste
        user_taste_X = user_info.X_taste
        user_taste_Y = user_info.Y_taste
        user_taste_Z = user_info.Z_taste
        user_type_A = user_info.A_type
        user_type_B = user_info.B_type
        user_type_C = user_info.C_type
        user_type_D = user_info.D_type
        dish_form = dishes.query.all()
        dish_order = {}
        for i in dish_form:
            point=0#计算总分
            a=0;b=0;c=0;d=0
            if i.info_taste_M == user_taste_M and user_taste_M==1:#compare and add point of
                point +=1
            if i.info_taste_N == user_taste_N and user_taste_N==1:
                point +=1
            if i.info_taste_X == user_taste_X and user_taste_X==1:
                point +=1
            if i.info_taste_Y == user_taste_Y and user_taste_Y==1:
                point +=1
            if i.info_taste_Z == user_taste_Z and user_taste_Z==1:
                point +=1
            if i.info_type == "appetizer":#record the type of dish
                a=1
            elif i.info_type == "soup":
                b=1
            elif i.info_type == "main course":
                c=1
            else:
                d=1
            if a == user_type_A and user_type_A==1:
                point +=2
            if b == user_type_B and user_type_B==1:
                point +=2
            if c == user_type_C and user_type_C==1:
                point +=2
            if d == user_type_D and user_type_D==1:
                point +=2
            dish_order[i.list_id] = point
        #排序
        dish_ordered = sorted(dish_order.items(),key=lambda x:x[1],reverse=True)
        opt1=list(dish_ordered.keys()[0])
        opt2=list(dish_ordered.keys()[1])
        opt3=list(dish_ordered.keys()[2])
        opt4="";opt5="";opt6=""
        for j in dish_form:
            if j.list_id==opt1:
                j.list_name=opt4
            if j.list_id==opt2:
                j.list_name=opt5
            if j.list_id==opt3:
                j.list_name=opt6
    return render_template("info.html",dish_id_1=opt1,dish_id_2=opt2,dish_id_3=opt3,dish_name_1 =opt4,dish_name_2=opt5,dish_name_3=opt6)

@app.route("/comment",methods=["GET","POST"])
def add_comment():
    dish_id = request.form.get("dish_id")
    if request.method=="POST":
        comment_info = request.form.get("message")
        current_time = datetime.datetime.now()
        QWQ = comment(dish_id=dish_id, Comment_Time=current_time, content=comment_info)
        db.session.add_all([QWQ])
        db.session.commit()
    if request.method=="GET":
        cmt= comment.query.filter_by(dish_id=dish_id).all()
    return render_template("comment",comment_info=cmt)

@app.route("/senior_add",methods=["GET","POST"])
def senior_add():
    if request.method == "POST":#add部分
        #生成新的id
        dish_list = dishes.query.filter_by(restaurant_id=1).all()
        last_dish_id = dish_list[-1].list_id
        new_dish_id = "A" + str(eval(last_dish_id[1:] + "+" + "1"))
        new_dish_name = request.form.get("dish_name")
        new_dish_description = request.form.get("dish_description")
        for n in dish_list:
            flag = False
            if n.list_name == new_dish_name:
                flash("Already have this meal")
                flag = True
        if flag == False:
            QOQ = dishes(list_id=new_dish_id, list_name=new_dish_name, info_description=new_dish_description)
            db.session.add_all([QOQ])
            db.session.commit()
            flash("successfully create one meal!")   
    return redirect(url_for('senior_r1'))

@app.route("/senior_delete"<rt1>,methods=["GET","POST"])#展示
def senior_delete():    
    if request.method == "GET":
        dish_table_1 = dishes.query.filter_by(restaurant_id=1).all()
    return redirect(url_for('senior_r1'))

@app.route("/senior_r1",methods=["GET","POST"])
def senior_r1():
    if request.method == "GET":
        dish_table_1 = dishes.query.filter_by(restaurant_id=1).all()
    return render_template("senior_r1",dish_table_ini=dish_table_1)

@app.route("/normal_r1")
def normal_r1():
    dish_table = dishes.query.filter_by(restaurant_id=1).all()
    return render_template("normal_r1.html",dish_table=dish_table)

db.drop_all()
db.create_all()

#为table加入数据
user1=common_user(common_name='zzz', common_password='12345')
user2=common_user(common_name='qqq', common_password='16949')
res1 = restaurants(restaurant_name = 'Membership restaurant',
    location = 'kitazawa',
    open_hour = '114154',
    meal_type = '1919810',
    average_price_per_person = 3.2,
    rate = 3)
senior_user1 = senior_user(senior_name='bizu',res_id=1,senior_password='114154')
db.session.add_all([user1, user2])
db.session.add_all([res1])
db.session.add_all([senior_user1])
db.session.commit()

if __name__ == '__main__':
    app.run()

