from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')

def index():

    name = 'Erfei'
    movies = [
        {'title': '大赢家', 'year': '2020'},
        {'title': '海贼王-顶上战争', 'year': '2019'},
        {'title': '囧妈', 'year': '2020'},
        {'title': '速度与激情8', 'year': '2019'},
        {'title': '战狼', 'year': '2019'},
    ]

    return render_template('index.html', name=name, movies=movies)


# # 动态路由
# @app.route('/index/<name>')
# def home(name):
#     return '<h1>hello %s</h1>'%name
