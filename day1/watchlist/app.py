# import os,sys
# from flask import Flask, render_template,flash,request,redirect,url_for
# import click
# from werkzeug.security import generate_password_hash,check_password_hash
# from flask_sqlalchemy import SQLAlchemy # 导入扩展类
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


# windows平台是三个/,其它(linux等)都是四个/
# WIN = sys.platform.startswith('win')
# if WIN:
#     prefix = 'sqlite:///'
# else:
#     prefix = 'sqlite:////'

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(app.root_path, 'data.db') #Linux
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db') # Windows
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭了对模型修改的监控
# app.config['SECRET_KEY'] = 'watchlist_dev'
# db = SQLAlchemy(app)   # 初始化扩展，传入程序实例app


# login_manager = LoginManager(app) # 实例化登录拓展类
# @login_manager.user_loader
# def load_user(user_id):
#     user = User.query.get(int(user_id))
#     return user
# login_manager.login_view = 'login'
# login_manager.login_message = '您还未登录'


# # 模板上下文处理函数
# @app.context_processor
# def common_user():
#     user = User.query.first()
#     return dict(user=user)



# 登录
# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         # 验证数据是否符合要求
#         if not username or not password:
#             flash('输入错误')
#             return redirect(url_for('login'))
#         # 和数据库中的信息进行比对验证
#         user = User.query.first()
#         if username==user.username and user.validate_password(password):
#             login_user(user)
#             flash('登录成功')
#             return redirect(url_for('index'))
#         flash('用户名或密码错误')
#         return redirect(url_for('login'))
#     return render_template('login.html')


# 登出
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('拜拜')
#     return redirect(url_for('index'))


# 设置
# @app.route('/settings',methods=['GET','POST'])
# @login_required
# def settings():
#     if request.method == 'POST':
#         name = request.form['name']
#         if not name or len(name)>20:
#             flash('输入错误')
#             return redirect(url_for('settings'))
#         current_user.name = name
#         db.session.commit()
#         flash('设置成功')
#         return redirect(url_for('index'))
#     return render_template('settings.html')


# 自定义命令
# @app.cli.command()  # 装饰器，可以注册命令
# @click.option('--drop', is_flag=True, help='删除后再创建')
# def initdb(drop):
#     if drop:
#         db.drop_all()
#     db.create_all()
#     click.echo('初始化数据库完成')





# 生成管理员用户
# @app.cli.command()
# @click.option('--username',prompt=True,help='管理员账号')
# @click.option('--password',prompt=True,help='管理员密码',hide_input=True,confirmation_prompt=True)
# def admin(username,password):
#     db.create_all()
#     user = User.query.first()
#     if user is not None:
#         click.echo('更新用户信息')
#         user.username = username
#         user.set_password(password)
#         db.session.add(user)
#     else:
#         click.echo('创建用户信息')
#         user = User(username=username,name='Admin')
#         user.set_password(password)
#         db.session.add(user)
#     db.session.commit()
#     click.echo('管理员创建完成')


# 错误处理函数
# @app.errorhandler(404)
# def page_not_found(e):
#     user = User.query.first()
#     # 返回模板和状态码
#     return render_template('404.html',user=user)






# # 动态路由
# @app.route('/index/<name>')
# def home(name):
#     return '<h1>hello %s</h1>'%name
