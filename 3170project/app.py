from flask import Flask, render_template, request, flash, url_for, redirect#request是一个请求对象
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import time
from flask import session
import os
from werkzeug.utils import secure_filename

#实现图片传输的设置
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__, template_folder='template', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
#

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@127.0.0.1/3170project'
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
    info_description = db.Column(db.String(500),unique=False,nullable=True)
    info_price = db.Column(db.String(10), unique=False, nullable=True)
    info_taste_M = db.Column(db.Integer, unique=False, nullable=True)
    info_taste_N = db.Column(db.Integer, unique=False, nullable=True)
    info_taste_X = db.Column(db.Integer, unique=False, nullable=True)
    info_taste_Y = db.Column(db.Integer, unique=False, nullable=True)
    info_taste_Z = db.Column(db.Integer, unique=False, nullable=True)
    restaurant_id = db.Column(db.Integer,unique=False, nullable=True)
    img_path = db.Column(db.String(128), unique=False, nullable=True)

class rate(db.Model):
    __tablename__="rate"
    restaurant_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    environment_rate = db.Column(db.Float(1), nullable=True)
    service_rate = db.Column(db.Float(1), nullable=True)
    taste_rate = db.Column(db.Float(1), nullable=True)
    price_rate = db.Column(db.Float(1), nullable=True)
    overall_rate = db.Column(db.Float(1), nullable=True)

class comments(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    # dish_id = db.Column(db.String(10),db.ForeignKey(dishes.list_id))
    dish_id = db.Column(db.String(10), unique=True, nullable=False)
    Comment_Time = db.Column(db.String(48), unique=True, nullable=False)#using the system time, you should import "datetime" and "time"
    content = db.Column(db.String(500))#free edit
    
class login_user(db.Model):#record the id of the user
    _tablename_="login_user"
    login_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    login_info=db.Column(db.Integer,nullable=False)
 
class current_dish(db.Model):#record the current dish that the user is viewing
    _tablename_="current_dish"
    dish_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    dish_info=db.Column(db.Integer,nullable=False)
    
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
            # user_id = db.session.execute("select info from login_user")#get user'sid
            user = login_user.query.first()
            user_id = user.login_info
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
            senior_info=senior_user.query.all()
            for y in senior_info:
                if y.senior_name == username:
                    resta_id = y.res_id
            dish_list=dishes.query.filter_by(restaurant_id=resta_id)
            if resta_id ==1:
                return redirect(url_for('senior_r1'))
            if resta_id == 2:
                return redirect(url_for('senior_r2'))
            if resta_id ==3:
                return redirect(url_for('senior_r3'))
            if resta_id ==4:
                return redirect(url_for('senior_r4'))
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
                    # user_list = common_user.query.all()

                    # last_user_id = user_list[-1]
                    # print(last_user_id)
                    # login_temp = common_user.query.filter_by(common_name=username).order_by(common_user.common_id.desc()).first()
                    # print(login_temp)
                    sub=common_user.query.all()
                    for x in sub:
                        if x.common_name == username:
                            id = x.common_id
                    login_status = login_user(login_info = id)
                    db.session.add_all([login_status])
                    db.session.commit()
                    return redirect(url_for("preference_record"))
                else:
                    flash('Password confirmation failed!')
            else:
                flash('Please enter the user name')
    return render_template('create_account.html')

@app.route('/main', methods=['GET', 'POST'])
def main():#餐厅系统主界面（餐厅列表页）
    a1=dishes.query.all()
    user = login_user.query.all()
    user_id=user[0].login_info
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
        elif i.info_type == "dessert":
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
    opt1=list(dish_ordered[0][0])
    opt2=list(dish_ordered[1][0])
    opt3=list(dish_ordered[2][0])
    opt4="";opt5="";opt6=""
    for j in dish_form:
        if j.list_id==opt1:
            j.list_name=opt4
        if j.list_id==opt2:
            j.list_name=opt5
        if j.list_id==opt3:
            j.list_name=opt6
    return render_template('info.html',a1=a1,dish_id_1=opt1,dish_id_2=opt2,dish_id_3=opt3,dish_name_1 =opt4,dish_name_2=opt5,dish_name_3=opt6)#主页面为info.html，传入参数a1(restaurant列表)

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



@app.route("/comment/<normal_send>",methods=["GET","POST"])
def comment(normal_send):
    dish_id = normal_send
    dish_table = dishes.query.get(dish_id)
    cmt= comments.query.filter_by(dish_id=normal_send).all()
    if request.method=="POST":
        comment_info = request.form.get("message")
        current_time = time.datetime.now()
        QWQ = comments(dish_id=dish_id, Comment_Time=current_time, content=comment_info)
        db.session.add_all([QWQ])
        db.session.commit()
        cmt= comments.query.filter_by(dish_id=normal_send).all()
        dish_table = dishes.query.get(dish_id)
    return render_template("comment.html",comment_table=cmt,dish_table=dish_table)

#this parts correspond to the 4 pages of senior, with 4*3 = 12 functions in total
#senior_r1
# @app.route("/senior_add1",methods=["GET","POST"])
# def senior_add1():
   
#     return redirect(url_for('senior_r1'))

@app.route("/senior_delete1/<senior_d>")
def senior_delete1(senior_d):    
    temp=dishes.query.filter_by(list_id=senior_d).first()
    if temp:
        try:
            db.session.delete(temp)
            db.session.commit()
            flash('Successfully delete!')
        except Exception as e:
            print (e)
            flash('Failed to delete')
            db.session.rollback
    else:
        flash('No this term')
    return redirect(url_for('senior_r1'))

@app.route("/senior_r1",methods=["GET","POST"])
def senior_r1():
    dish_table_1 = dishes.query.filter_by(restaurant_id=1).all()
    if request.method == "POST":#add part
        #generate new id
        dish_list = dishes.query.filter_by(restaurant_id=1).all()
        last_dish_id = dish_list[-1].list_id
        new_dish_id = "A" + str(eval(last_dish_id[1:] + "+" + "1"))
        new_dish_name = request.form.get("dish_name")
        new_dish_description = request.form.get("dish_description")
        new_dish_price=request.form.get("dish_price")
        new_dish_image= request.files['uploaded_file']#传入图片的参数名
        for n in dish_list:
            flag = False
            if n.list_name == new_dish_name:
                flash("Already have this meal")
                flag = True
        if flag == False:
            #图片保存路径
            new_img_name = new_dish_id + ".png"
            base_path = basedir + "/static/uploads/"
            new_path = base_path + new_img_name
            new_dish_image.save(new_path)
            # path = os.path.join(UPLOAD_FOLDER, new_img_name)
            # new_dish_image.save(path)
            # new_img_path = os.path.join(UPLOAD_FOLDER, new_img_name)
            new_img_path = new_path
            #
            QOQ = dishes(list_id=new_dish_id, list_name=new_dish_name, info_description=new_dish_description, info_price=new_dish_price, img_path=new_img_path)
            db.session.add_all([QOQ])
            db.session.commit()
            flash("successfully create one meal!")    
    return render_template("senior_r1.html",dish_table=dish_table_1)
#senior_r2
# @app.route("/senior_add2",methods=["GET","POST"])
# def senior_add2():
 
#     return redirect(url_for('senior_r2'))

@app.route("/senior_delete2/<senior_d>")
def senior_delete2(senior_d):    
    temp=dishes.query.filter_by(list_id=senior_d).first()
    if temp:
        try:
            db.session.delete(temp)
            db.session.commit()
            flash('Successfully delete!')
        except Exception as e:
            print (e)
            flash('Failed to delete')
            db.session.rollback
    else:
        flash('No this term')
    return redirect(url_for('senior_r2'))

@app.route("/senior_r2",methods=["GET","POST"])
def senior_r2():
    dish_table_1 = dishes.query.filter_by(restaurant_id=2).all()
    if request.method == "POST":#add部分
        #生成新的id
        dish_list = dishes.query.filter_by(restaurant_id=2).all()
        last_dish_id = dish_list[-1].list_id
        new_dish_id = "B" + str(eval(last_dish_id[1:] + "+" + "1"))
        new_dish_name = request.form.get("dish_name")
        new_dish_description = request.form.get("dish_description")
        new_dish_price=request.form.get("dish_price")
        new_dish_image= request.form.get("uploaded_file")
        for n in dish_list:
            flag = False
            if n.list_name == new_dish_name:
                flash("Already have this meal")
                flag = True
        if flag == False:
            new_img_name = new_dish_id + ".png"
            new_dish_image.save(os.path.join(app.config['UPLOAD_FOLDER'], new_img_name))
            new_img_path = os.path.join(app.config['UPLOAD_FOLDER'], new_img_name)
            QOQ = dishes(list_id=new_dish_id, list_name=new_dish_name, info_description=new_dish_description, info_price=new_dish_price, img_path=new_img_path)
            db.session.add_all([QOQ])
            db.session.commit()
            flash("successfully create one meal!")      
    return render_template("senior_r2.html",dish_table=dish_table_1)
#senior_r3
# @app.route("/senior_add3",methods=["GET","POST"])
# def senior_add3():
 
#     return redirect(url_for('senior_r3'))

@app.route("/senior_delete3/<senior_d>")
def senior_delete3(senior_d):    
    temp=dishes.query.filter_by(list_id=senior_d).first()
    if temp:
        try:
            db.session.delete(temp)
            db.session.commit()
            flash('Successfully delete!')
        except Exception as e:
            print (e)
            flash('Failed to delete')
            db.session.rollback
    else:
        flash('No this term')
    return redirect(url_for('senior_r3'))

@app.route("/senior_r3",methods=["GET","POST"])
def senior_r3():
    dish_table_1 = dishes.query.filter_by(restaurant_id=3).all()
    if request.method == "POST":#add部分
        #生成新的id
        dish_list = dishes.query.filter_by(restaurant_id=3).all()
        last_dish_id = dish_list[-1].list_id
        new_dish_id = "C" + str(eval(last_dish_id[1:] + "+" + "1"))
        new_dish_name = request.form.get("dish_name")
        new_dish_description = request.form.get("dish_description")
        new_dish_price=request.form.get("dish_price")  
        new_dish_image= request.form.get("uploaded_file")      
        for n in dish_list:
            flag = False
            if n.list_name == new_dish_name:
                flash("Already have this meal")
                flag = True
        if flag == False:
            new_img_name = new_dish_id + ".png"
            new_dish_image.save(os.path.join(app.config['UPLOAD_FOLDER'], new_img_name))
            new_img_path = os.path.join(app.config['UPLOAD_FOLDER'], new_img_name)
            QOQ = dishes(list_id=new_dish_id, list_name=new_dish_name, info_description=new_dish_description, info_price=new_dish_price, img_path=new_img_path)
            db.session.add_all([QOQ])
            db.session.commit()
            flash("successfully create one meal!")      
    return render_template("senior_r3.html",dish_table=dish_table_1)
#senior_r4
# @app.route("/senior_add4",methods=["GET","POST"])
# def senior_add4():
  
#     return redirect(url_for('senior_r4'))

@app.route("/senior_delete4/<senior_d>")
def senior_delete4(senior_d):    
    temp=dishes.query.filter_by(list_id=senior_d).first()
    if temp:
        try:
            db.session.delete(temp)
            db.session.commit()
            flash('Successfully delete!')
        except Exception as e:
            print (e)
            flash('Failed to delete')
            db.session.rollback
    else:
        flash('No this term')
    return redirect(url_for('senior_r4'))

@app.route("/senior_r4",methods=["GET","POST"])
def senior_r4():
    dish_table_1 = dishes.query.filter_by(restaurant_id=4).all()
    if request.method == "POST":#add部分
        #生成新的id
        dish_list = dishes.query.filter_by(restaurant_id=4).all()
        last_dish_id = dish_list[-1].list_id
        new_dish_id = "D" + str(eval(last_dish_id[1:] + "+" + "1"))
        new_dish_name = request.form.get("dish_name")
        new_dish_description = request.form.get("dish_description")
        new_dish_price=request.form.get("dish_price")  
        new_dish_image= request.form.get("uploaded_file")      
        for n in dish_list:
            flag = False
            if n.list_name == new_dish_name:
                flash("Already have this meal")
                flag = True
        if flag == False:
            new_img_name = new_dish_id + ".png"
            new_dish_image.save(os.path.join(app.config['UPLOAD_FOLDER'], new_img_name))
            new_img_path = os.path.join(app.config['UPLOAD_FOLDER'], new_img_name)
            QOQ = dishes(list_id=new_dish_id, list_name=new_dish_name, info_description=new_dish_description, info_price=new_dish_price, img_path=new_img_path)
            db.session.add_all([QOQ])
            db.session.commit()
            flash("successfully create one meal!") 
    return render_template("senior_r4.html",dish_table=dish_table_1)
#senior部分结束

#the normal parts start，4 functions in total
@app.route("/normal_r1")
def normal_r1():
    dish_table = dishes.query.filter_by(restaurant_id=1).all()
    return render_template("normal_r1.html",dish_table=dish_table)

@app.route("/normal_r2")
def normal_r2():
    dish_table = dishes.query.filter_by(restaurant_id=2).all()
    return render_template("normal_r2.html",dish_table=dish_table)

@app.route("/normal_r3")
def normal_r3():
    dish_table = dishes.query.filter_by(restaurant_id=3).all()
    return render_template("normal_r3.html",dish_table=dish_table)

@app.route("/normal_r4")
def normal_r4():
    dish_table = dishes.query.filter_by(restaurant_id=4).all()
    return render_template("normal_r4.html",dish_table=dish_table)
#normal部分结束

db.drop_all()
db.create_all()

#initialized the database
user1=common_user(common_name='zzz', common_password='12345')
user2=common_user(common_name='qqq', common_password='16949')
res1 = restaurants(restaurant_name = 'Membership restaurant',
    location = 'kitazawa',
    open_hour = '114154',
    meal_type = '1919810',
    average_price_per_person = 3.2,
    rate = 3)
senior_user1 = senior_user(senior_name='bizu',res_id=1,senior_password='114154')

dish_a1=dishes(list_id='A1',list_name="Cream Stew", info_type="soup", info_description="A meat and vegetable stew. These warm, buttery ingredients are so good that you almost want to dive into the cream stew and cuddle up with them.",
    info_price="$25", info_taste_M=1, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=1, img_path="/static/uploads/A1.png")
dish_a2=dishes(list_id='A2',list_name="Fruit of the Festival", info_type="dessert", info_description="The sublime enjoyment brought by the refreshing taste is almost like a sweet, illusory dream. One small sip transports you onto a white, sandy beach, where the sparkling seawater beats with the rhythm to which the hymn of your leisurely vacation shall be composed.",
    info_price="$12", info_taste_M=1, info_taste_N=1, info_taste_X=0, info_taste_Y=0, info_taste_Z=0, restaurant_id=1, img_path="/static/uploads/A2.png")
dish_a3=dishes(list_id='A3',list_name="Goulash", info_type="soup", info_description="A steaming-hot stew. Just one spoonful sends a down-to-earth sense of satisfaction welling up from the depth of your heart. The meat's flavor grows with every chew, bring limitless strength to the eater even in the coldest wintry wastes.",
    info_price="$25", info_taste_M=0, info_taste_N=1, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=1, img_path="/static/uploads/A3.png")
dish_a4=dishes(list_id='A4',list_name="Moon Pie", info_type="appetizer", info_description="A traditional staple. As you cut a slice off this small meat pie, the aromas of butter and meat assault your senses simultaneously. The rustic, sweet mouthfeel reminds you of the sights and sounds of harvest festivals, bringing a smile unbidden to your face.",
    info_price="$20", info_taste_M=1, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=1, img_path="/static/uploads/A4.png")
dish_a5=dishes(list_id='A5',list_name="Mushroom Pizza", info_type="main course", info_description="A pizza covered in cheese and mushrooms. It's a party in your month and the cheese and mushrooms invited all their delicious friends.",
    info_price="$25", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=1, img_path="/static/uploads/A5.png")
dish_a6=dishes(list_id='A6',list_name="Sticky Honey Roast", info_type="main course", info_description="A meat dish in a sweet honey sauce. The warm honey draws out the flavor of the meat, creating a flavor explosion akin to bathing in the warm summer sun.",
    info_price="$27", info_taste_M=1, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=1, img_path="/static/uploads/A6.png")
dish_a7=dishes(list_id='A7',list_name="Sunshine Sprat", info_type="main course", info_description="Gently fried fish dish. The fish melts in your mouth, melding the flavors of land and sea together as it does, making for an unforgettable experience. Little wonder, then, that such as simply-made dish can make it into restaurants of great class.",
    info_price="$12", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=1, img_path="/static/uploads/A7.png")
dish_a8=dishes(list_id='A8',list_name="Sweet Madame", info_type="main course", info_description="Honey-roasted fowl. Tender and sweet, the meat has perfectly fused with honey, ensuring the only thing left of the dish will be the cleanly-picked bones.",
    info_price="$23", info_taste_M=1, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=1, img_path="/static/uploads/A8.png")

dish_b1=dishes(list_id='B1',list_name="Adeptus' Temptation", info_type="soup", info_description="The dish is a rare and exquisite mix of both land and the sea, combining countless delicious delicacies in one flavor-filled pot. Each mouthful is a moment to remember - it's even irresistible enough to entice the adepti down from their celestial abode.",
    info_price="$59", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=2, img_path="/static/uploads/B1.png")
dish_b2=dishes(list_id='B2',list_name="Almond Tofu", info_type="dessert", info_description="The dish is a rare and exquisite mix of both land and the sea, combining countless delicious delicacies in one flavor-filled pot. Each mouthful is a moment to remember - it's even irresistible enough to entice the adepti down from their celestial abode.",
    info_price="$12", info_taste_M=1, info_taste_N=0, info_taste_X=0, info_taste_Y=0, info_taste_Z=0, restaurant_id=2, img_path="/static/uploads/B2.png")
dish_b3=dishes(list_id='B3',list_name="Bamboo Shoot Soup", info_type="soup", info_description="A soup dish that's been stewed for a long while. One whiff is enough to whet one's appetite greatly, and the concentrated flavors fill you body with every spoonful of soup. It is almost like spreading a pair of wings and walking on clouds.",
    info_price="$14", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=2, img_path="/static/uploads/B3.png")
dish_b4=dishes(list_id='B4',list_name="Black-Back Perch Stew", info_type="appetizer", info_description="A poached fish dish. The fish fillets are so tender and juicy that they almost seem to come alive in your mouth. The sense of loss is so unbearable that when you swallow a piece down, you just have to treat yourself to another.",
    info_price="$22", info_taste_M=0, info_taste_N=0, info_taste_X=1, info_taste_Y=1, info_taste_Z=1, restaurant_id=2, img_path="/static/uploads/B4.png")
dish_b5=dishes(list_id='B5',list_name="Chili-Mince Cornbread Buns", info_type="main course", info_description="The intense charred aroma of the wok sits on the condiments, which are shoveled into the fluffy buns, filling the air with a fragrance that itself worth rave reviews. No wonder such a dish could even awaken a sleeping god…",
    info_price="$30", info_taste_M=0, info_taste_N=0, info_taste_X=1, info_taste_Y=1, info_taste_Z=0, restaurant_id=2, img_path="/static/uploads/B5.png")
dish_b6=dishes(list_id='B6',list_name="Crystal Shrimp", info_type="appetizer", info_description="The outer skin is as clear its crystal namesake, and when it enters the mouth, one's tongue could be forgiven for thing that the fresh shrimp within is still alive. Those who eat it can only lament that four pieces per serving is far, far too few.",
    info_price="$19", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=2, img_path="/static/uploads/B6.png")
dish_b7=dishes(list_id='B7',list_name="Noodles with Deliciacies", info_type="main course", info_description="Noodles in a meat and vegetable sauce. The seemingly ordinary noodles have absorbed the essence of the mountainous delicacies. A single mouthful is enough to taste its extreme freshness.",
    info_price="$13", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=2, img_path="/static/uploads/B7.png")
dish_b8=dishes(list_id='B8',list_name="Vegetarian Abalone", info_type="appetizer", info_description="A vegetarian dish with a rich flavor. With the aid of the sauce, the matsutake has achieved an excellent, elegant mouth-feel that so rivals scallop in tenderness and abalone in freshness that you can hardly tell them apart.",
    info_price="$12", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=2, img_path="/static/uploads/B8.png")
    
dish_c1=dishes(list_id='C1',list_name="Imported Poultry", info_type="appetizer", info_description="Having been marinated beforehand, the fowl has had several layers of flavor added to it, keeping its oiliness in perfect moderation. Bite down on that crispy, crackling, flour-skin, and feel the rich juices of the fowl rush into your mouth and whet your appetite.",
    info_price="$18", info_taste_M=0, info_taste_N=1, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=3, img_path="/static/uploads/C1.png")
dish_c2=dishes(list_id='C2',list_name="More-and-More", info_type="main course", info_description="A snack grilled on an iron plate. The rich ingredients have been stacked atop one another. One bite into the crisp outer layer reveals the soft tenderness within. The lovely sauce clothes the condiments luxuriously, flowing between lips and teeth alike en route to the stomach.",
    info_price="$19", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=3, img_path="/static/uploads/C2.png")
dish_c3=dishes(list_id='C3',list_name="Rice Cake Soup", info_type="soup", info_description="Commonly-seen city cuisine. The freshness of light soup forms the perfect backdrop for the original flavor of the ingredients to stand out. This back-to-basics cuisine is sure to make you feel warm inside when eaten on a snowy night.",
    info_price="$26", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=3, img_path="/static/uploads/C3.png")
dish_c4=dishes(list_id='C4',list_name="Sakura Mochi", info_type="dessert", info_description="It is surrounded by the fragrance of sakura, and its elegant exterior hides a loveliness that comes forth and disappears in the a single instant. In a moment when all is silent, a single taste returns you to the moment when the sakura were as a blizzard all about you.",
    info_price="$12", info_taste_M=1, info_taste_N=0, info_taste_X=0, info_taste_Y=0, info_taste_Z=0, restaurant_id=3, img_path="/static/uploads/C4.png")
dish_c5=dishes(list_id='C5',list_name="Sakura Tempura", info_type="appetizer", info_description="A dish deep-fried in oil. The batter is thin and sheer, like as set of luxurious clothes over the ingredients. The outside crispness and freshness within form amazing layers of texture, leading those who eat it to marvel at just how this delicacy was created.",
    info_price="$20", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=3, img_path="/static/uploads/C5.png")
dish_c6=dishes(list_id='C6',list_name="Sashimi Platter", info_type="appetizer", info_description="A seafood dish made using fresh ingredients. The plate spread before you is like a work of art, almost too beautiful to shatter. The surpassing knife-work has imparted the greatest mouthfeel upon the ingredients possible.",
    info_price="$19", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=3, img_path="/static/uploads/C6.png")
dish_c7=dishes(list_id='C7',list_name="Tonkotsu Ramen", info_type="main course", info_description="The springy noodles have absorbed the essence of the soup, and the accoutrements have added all manner of variation to the mouthfeel. The soup has preserved the strong fragrance of the bones used to make it, yet does down gently without that greasy feeling.",
    info_price="$15", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=3, img_path="/static/uploads/C7.png")
dish_c8=dishes(list_id='C8',list_name="Unagi Chazuke", info_type="main course", info_description="A light and tasty main dish. The tea and soup weave an elegant, fragrant melody punctuated by the pure white grains, while the unagi, baptized in coal-fired, provides tender, gentle decoration to the mix.",
    info_price="$13", info_taste_M=0, info_taste_N=0, info_taste_X=0, info_taste_Y=1, info_taste_Z=1, restaurant_id=3, img_path="/static/uploads/C8.png")

dish_d1=dishes(list_id='D1',list_name="Butter Chicken", info_type="appetizer", info_description="A flavorful dish. Juicy chicken is saturated with silky sauce. Every bite orchestrates an “elemental symphony of flavors” … Oops, before you even knew it, you had already emptied the plate. Dip the flatbread in the sauce - every last drop of this must go!",
    info_price="$15", info_taste_M=0, info_taste_N=0, info_taste_X=1, info_taste_Y=1, info_taste_Z=0, restaurant_id=4, img_path="/static/uploads/D1.png")
dish_d2=dishes(list_id='D2',list_name="Masala Cheese Ball", info_type="soup", info_description="The spices were mixed with the other ingredients in a special way to bring out the most original scents. They awaken your taste buds and create a multi-layered flavor profile. The cheese balls are crispy on the outside and soft on the inside.",
    info_price="$17", info_taste_M=0, info_taste_N=0, info_taste_X=1, info_taste_Y=1, info_taste_Z=0, restaurant_id=4, img_path="/static/uploads/D2.png")
dish_d3=dishes(list_id='D3',list_name="Padisarah Pudding", info_type="dessert", info_description="The moment it enters your mouth, the springy mouthfeel makes you feel like you're wandering atop milk-flavored clouds. As you savor its flavors, the blended fragrance of Padisarah and rose fills the air.",
    info_price="$10", info_taste_M=1, info_taste_N=0, info_taste_X=0, info_taste_Y=0, info_taste_Z=0, restaurant_id=4, img_path="/static/uploads/D3.png")
dish_d4=dishes(list_id='D4',list_name="Panipuri", info_type="appetizer", info_description="Anticipate the mysterious, bright-colored juice within, and bring it to your mouth - the coolness, sourness, and tingling sensation re bouncing freely on your tongue as if someone has ignited a stick of dreamy dynamite.",
    info_price="$20", info_taste_M=0, info_taste_N=1, info_taste_X=1, info_taste_Y=1, info_taste_Z=0, restaurant_id=4, img_path="/static/uploads/D4.png")
dish_d5=dishes(list_id='D5',list_name="Samosa", info_type="appetizer", info_description="A deep-fried snack. Each golden, crispy pocket is stuffed full with a soft, glutinous filling. You can't help but wolf one down immediately, and then reach out for a second one, taking your time to savor it...",
    info_price="$19", info_taste_M=0, info_taste_N=1, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=4, img_path="/static/uploads/D5.png")
dish_d6=dishes(list_id='D6',list_name="Selva Salad", info_type="appetizer", info_description="Crispy and juicy Zaytun Peaches are served with fresh mints and blooming roses. This delicacy tastes refreshingly sweet and feels pleasantly cool on the tongue.",
    info_price="$10", info_taste_M=1, info_taste_N=1, info_taste_X=0, info_taste_Y=0, info_taste_Z=0, restaurant_id=4, img_path="/static/uploads/D6.png")
dish_d7=dishes(list_id='D7',list_name="Shawarma Wrap", info_type="appetizer", info_description="A wrap filled with roasted meat. On the thin, soft flatbread lies the tender meat covered in a crispy exterior, and the flavor is enriched by spices and balanced by vegetables. A small mouthful is enough to please one's picky taste buds.",
    info_price="$12", info_taste_M=0, info_taste_N=0, info_taste_X=1, info_taste_Y=1, info_taste_Z=0, restaurant_id=4, img_path="/static/uploads/D7.png")
dish_d8=dishes(list_id='D8',list_name="Tahchin", info_type="main course", info_description="A classic rice dish served in large quantities. With the first bite, the crispy outside cracks with delightful crunching sounds. The second bite combines the soft and moist rice with juicy meat in your mouth.",
    info_price="$18", info_taste_M=0, info_taste_N=1, info_taste_X=0, info_taste_Y=1, info_taste_Z=0, restaurant_id=4, img_path="/static/uploads/D8.png")
    
db.session.add_all([user1, user2])
db.session.add_all([res1])
db.session.add_all([senior_user1])
db.session.add_all([dish_a1,dish_a2,dish_a3,dish_a4,dish_a5,dish_a6,dish_a7,dish_a8])
db.session.add_all([dish_b1,dish_b2,dish_b3,dish_b4,dish_b5,dish_b6,dish_b7,dish_b8])
db.session.add_all([dish_c1,dish_c2,dish_c3,dish_c4,dish_c5,dish_c6,dish_c7,dish_c8])
db.session.add_all([dish_d1,dish_d2,dish_d3,dish_d4,dish_d5,dish_d6,dish_d7,dish_d8])
db.session.commit()

if __name__ == '__main__':
    app.run()

