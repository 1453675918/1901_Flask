import os,sys


from flask import Flask, render_template
import click
from flask_sqlalchemy import SQLAlchemy


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
db = SQLAlchemy(app)   # 初始化扩展，传入程序实例app


# models
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

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
@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


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
