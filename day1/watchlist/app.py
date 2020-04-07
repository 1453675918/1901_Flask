import os,sys


from flask import Flask, render_template,flash,request,redirect,url_for
import click
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


# windows平台是三个/,其它(linux等)都是四个/
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(app.root_path, 'data.db') #Linux
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db') # Windows
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭了对模型修改的监控
app.config['SECRET_KEY'] = 'watchlist_dev'
db = SQLAlchemy(app)   # 初始化扩展，传入程序实例app


login_manager = LoginManager(app) # 实例化登录拓展类
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user
login_manager.login_view = 'login'
login_manager.login_message = '您还未登录'

# models
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# 模板上下文处理函数
@app.context_processor
def common_user():
    user = User.query.first()
    return dict(user=user)


# views
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据是否符合要求
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('不能为空或超过最大长度')
            return redirect(url_for('index'))
        # 保存表单数据
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('创建成功')
        return redirect(url_for('index'))
    else:
        user = User.query.first()
        movies = Movie.query.all()
        return render_template('index.html', user=user, movies=movies)


@app.route('/movie/edit/<int:movies_id>',methods=['GET','POST'])
@login_required
def edit(movies_id):
    movie = Movie.query.get_or_404(movies_id)
    print(movie)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        # 验证数据是否符合要求
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('不能为空或超过最大长度')
            return redirect(url_for('index'), movie_id=movies_id)
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('更新完成')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)


# 删除
@app.route('/movie/delete/<int:movies_id>',methods=['POST'])
@login_required
def delete(movies_id):
    movie = Movie.query.get_or_404(movies_id)
#么有就404
    db.session.delete(movie)
    db.session.commit()
    flash("数据删除成功")
    return redirect(url_for('index'))


# 登录
# 登录
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method =="POST":
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash("输入错误")
            return redirect(url_for('login'))
        user = User.query.first()
        # 验证用户名和密码是否一致
        if username==user.username and user.validate_password(password):
            login_user(user)
            flash("登录成功")
            return redirect(url_for('index'))
        flash('用户名或密码错误')
        return redirect(url_for('login'))
    return render_template('login.html')
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
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('拜拜')
    return redirect(url_for('index'))


# 设置
@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name)>20:
            flash('输入错误')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('设置成功')
        return redirect(url_for('index'))
    return render_template('settings.html')


# 自定义命令
@app.cli.command()  # 装饰器，可以注册命令
@click.option('--drop', is_flag=True, help='删除后再创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库完成')


# 初始化数据库
@app.cli.command()
def forge():
    name = 'erfei'
    movies = [
        {'title': '大赢家', 'year': '2020'},
        {'title': '海贼王-顶上战争', 'year': '2019'},
        {'title': '囧妈', 'year': '2020'},
        {'title': '速度与激情8', 'year': '2019'},
        {'title': '战狼', 'year': '2019'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('导入数据库')


# 生成管理员用户
@app.cli.command()
@click.option('--username',prompt=True,help='管理员账号')
@click.option('--password',prompt=True,help='管理员密码',hide_input=True,confirmation_prompt=True)
def admin(username,password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('更新用户信息')
        user.username = username
        user.set_password(password)
        db.session.add(user)
    else:
        click.echo('创建用户信息')
        user = User(username=username,name='Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('管理员创建完成')


# 错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    # 返回模板和状态码
    return render_template('404.html',user=user)






# # 动态路由
# @app.route('/index/<name>')
# def home(name):
#     return '<h1>hello %s</h1>'%name
