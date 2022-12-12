from flask import Flask, render_template, request, flash, url_for, redirect#request是一个请求对象
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
# from flask_wtf import FlaskForm#wtf拓展的表单格式
# from wtforms import SubmitField, PasswordField, StringField#表单字段类别
# from wtforms.validators import EqualTo, DataRequired#表单验证函数

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@127.0.0.1/flaskproj3'#进入mysql账号，进入本地回传IP，连接先前建立好的数据库”flaskproj3“
app.secret_key='bilibili'#使用flash必须要设置密匙，内容随意


class table1(db.Model):#数据库模型，继承自db.Model，用户信息，和table2,table3是独立的
    #定义表名
    __tablename__="users"
    #定义内容
    user_id=db.Column(db.Integer,primary_key=True)#新建列，主键不重复且自增
    user_name=db.Column(db.String(32),unique=True,nullable=False)
    user_password = db.Column(db.String(255),nullable=False)
    # user_type = db.Column(db.String(10))

class table2(db.Model):#专家信息
    __tablename__="infos"
    info_id=db.Column(db.Integer,primary_key=True)
    info_item = db.Column(db.String(255))#项目或工作
    info_address = db.Column(db.String(255))
    info_status = db.Column(db.String(16))#职称
    info_org = db. Column(db.String(16))#机构
    info_key=db.Column(db.Integer, db.ForeignKey('namelist.list_id'))#外键需要绑定table3”name“的主键list_id, 外键设在多的一方

class table3(db.Model):#专家姓名
    __tablename__="namelist"
    list_id = db.Column(db.Integer,primary_key=True)
    list_name = db.Column(db.String(16), unique=True)
    info_ref = db.relationship('table2', backref='name_ref')#关系引用，要求必须先在两表间建立外键作为链接，info_ref是给table3用的，name_ref是给table2用的（反引用）

@app.route('/', methods=['GET', 'POST'])#route指明函数路由
def index():  # 密码登录程序
    #判断网页请求类型
    if request.method=="POST":
        #获取数据
        username=request.form.get('username')
        password=request.form.get('password')
        #处理数据，验证密码和账户
        check1=table1.query.all()
        checka=0
        checkb=0
        for i in check1:
            if i.user_name==username:#在循环中遍历数据库检索有没有匹配项
                checka=1
                if i.user_password==password:
                    checkb=1
                else:
                    checkb=0
            else:
                checka=0
            if checka==1:
                break
        if checka != 1:
            flash(u'账户错误')#flash的信息会显示在网页上，和return还有print有区别.，u用于正确编码信息
        elif checkb != 1:
            flash(u"密码错误")#flash可以加密，比单纯的return传参数更安全，信息直接传回模板，需设置secret key才能用
        else:
            return redirect(url_for('info'))#重定向，是根据函数名定向而不是路由名，虽然一般路由名等于函数名，此时跳转到info函数及其相应页面
    return render_template("login.html")

@app.route('/info', methods=['GET', 'POST'])
def info():#数据库信息界面
    a1=table3.query.all()#查询表中所有元素，并保存为a1，不需要查询table2是因为有引用链接
    if request.method=='POST':
        check2=0#检测专家名，记录id
        check3=0#检测项目是否重复
        check4=0#检测是否成功添加
        rt1=request.form.get('expname')#从表单中根据名称获取相应输入
        rt2=request.form.get('expstatus')
        rt3=request.form.get('expproj')
        rt4=request.form.get('expaddr')
        for i in a1:
            check2=1
            if i.list_name==rt1:#专家名是否相同
                check2=i.list_id
                for j in i.info_ref:#若相同则进入每个人的项目信息
                    if j.info_item==rt3:#项目名称若相同则判定为重复输入
                        check3=1
                        break
            else:
                check2=0
                continue
        if check3==1:
            flash(u"已有项目！")
        else:
            if check2!=0:#单人多项目
                try:
                    rt6 = table2(info_item=rt3, info_status=rt2, info_address=rt4, info_key=check2)#需要将该行的每一项填上
                    db.session.add_all([rt6])
                    db.create_all()
                    db.session.commit()
                except Exception as e:
                    print (e)
                    flash ("添加信息失败")
                    db.session.rollback()#回滚数据库
                    check4=1
            else:#若先前没有该专家才进行添加，否则跳过
                try:
                    rt5=table3(list_name=rt1)
                    db.session.add_all([rt5])#一个添加，如rt5和rt6，相当于一个主键(primary_key)下的所有内容（在这里等于表的一行）
                    db.session.commit()
                    rt6=table2(info_item=rt3, info_status=rt2, info_address=rt4, info_key=rt5.list_id)#将外键接到另一张表的主键上，该行内容的引用链接才会成立
                    db.session.add_all([rt6])
                    db.create_all()
                    db.session.commit()
                except Exception as e:
                    print (e)
                    flash ("无法添加专家及其信息")
                    db.session.rollback()
                    check4=1
            if check4!=1:
                a1 = table3.query.all()
                flash(u'提交成功！')
            else:
                pass
    return render_template('expert_info.html', a1=a1)#a1传递进expert_info页面

#删除专家信息
@app.route('/delete_info/<rt7_id>')#尖括号内为接受参数，按主键id找到内容并删除，rt7_id是html端传入的，为该项信息的info_id
def delete_info(rt7_id):#函数接收传入参数
    check5=table2.query.get(rt7_id)#在数据库中查询是否有该信息的id
    if check5:#有该信息，此时check5即为该项的代名，由此进行删除操作
        try:
            db.session.delete(check5)
            db.session.commit()
            flash("删除成功！")
        except Exception as e:
            print (e)
            flash("删除操作出错")
            db.session.rollback()
    else:
        flash('无此信息项目')

    return redirect(url_for('info'))#操作返回info，页面文件为expert_info.html

#删除专家
@app.route('/delete_exp/<rt8_nameid>')
def delete_exp(rt8_nameid):
    check6=table3.query.get(rt8_nameid)#作者是否存在，若存在，check6即为该项名称
    if check6:
        try:
            #先删专家信息再删专家，信息可以在查询之后直接delete()删除
            table2.query.filter_by(info_key=check6.list_id).delete()
            db.session.delete(check6)
            db.session.commit()
            flash('删除成功！')
        except Exception as e:
            print (e)
            flash("删除操作出错")
            db.session.rollback()
    else:
        flash('无此作者')
    return redirect(url_for('info'))

@app.route('/user_create', methods=['GET', 'POST'])
def user_create():
    if request.method=="POST":
        username=request.form.get('username')
        pw=request.form.get('password')
        pw2=request.form.get('password2')
        check7=table1.query.filter_by(user_name=username).first()#筛选filter_by，检测table1中是否已存在该用户名
        if check7:
            flash('用户已存在')
        else:
            if len(username)!=0:
                if pw==pw2 and len(pw)!=0:
                    user=table1(user_name=username, user_password=pw)
                    db.session.add_all([user])
                    db.session.commit()
                    flash('创建用户成功！')
                else:
                    flash('密码确认失败！')
            else:
                flash('请输入用户名')
    return render_template('create.html')


db.drop_all()
db.create_all()
#为table加入数据
user1=table1(user_name='zzz', user_password='12345')
user2=table1(user_name='qqq', user_password='16949')
db.session.add_all([user1, user2])
db.session.commit()
exp1=table3(list_name="张三")
exp2=table3(list_name="李四")
exp3=table3(list_name="王五")
db.session.add_all([exp1, exp2, exp3])
db.session.commit()
infoa=table2(info_item="研究开发", info_status="教授", info_address="柳州", info_key=exp1.list_id)#将外键接到另一张表元素的主键上，该行内容的引用链接才会成立
infob=table2(info_item="硬件维护", info_status="技术员", info_address="广州", info_key=exp2.list_id)
infoc=table2(info_item="资金管理", info_status="经理", info_address="香港", info_key=exp2.list_id)
infod=table2(info_item="运维", info_status="研究生", info_address="重庆", info_key=exp3.list_id)
db.session.add_all([infoa, infob, infoc, infod])
db.session.commit()


if __name__ == '__main__':
    app.run()