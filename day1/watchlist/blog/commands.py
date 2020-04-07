import click

from blog import db,app
from blog.models import User, Movies


@app.cli.command()
@click.option('--drop', is_flag=True, help='删除创建')
def initdb(drop):
    if drop:
        db.drop_all()
        click.echo('重新创建')
    db.create_all()

# @app.cli.command()
# def foreg():
#     name = 'zhaohuizhe'
#     movies = [
#         {
#             "title": "大赢家",
#             "year": "2020"
#         },
#         {
#             "title": "囧妈",
#             "year": "2000"
#         },
#         {
#             "title": "战狼",
#             "year": "2018"
#         },
#         {
#             "title": "心花怒放",
#             "year": "2017"
#         },
#         {
#             "title": "速度与激情",
#             "year": "2019"
#         },
#         {
#             "title": "我的父亲母亲",
#             "year": "2010"
#         },
#     ]
#     user = User(name=name)
#     db.session.add(user)
#     for m in movies:
#         movie = Movies(title=m['title'], year=m['year'])
#         db.session.add(movie)
    
#     db.session.commit()
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
        movie = Movies(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('导入数据库')

@app.cli.command()
@click.option('--username', prompt=True, help='管理员账号')
@click.option('--password', prompt=True, help='管理员密码', hide_input=True, confirmation_prompt=True)
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('更新用户信息')
        user.username = username
        user.set_password(password)
        db.session.add(user)
    else:
        click.echo('创建用户信息')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()