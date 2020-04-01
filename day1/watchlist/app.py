from flask import Flask
app = Flask(__name__)

@app.route('/')

def index():

    return '<h1>hello Flask 111</h1>'


# 动态路由
@app.route('/index/<name>')
def home(name):
    return '<h1>hello %s</h1>'%name
