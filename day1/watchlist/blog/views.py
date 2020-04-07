from flask import redirect, render_template, flash, request
from blog import db,app
from blog.models import User, Movies
from flask_login import LoginManager, login_required, current_user, logout_user, login_user


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(title) > 20 or len(year) > 4:
            flash('不能超过最大长度或为空')
            return redirect(url_for('index'))
        
        movie = Movies(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('创建成功')
            
    movies = Movies.query.all()
    return render_template('index.html', movies=movies)
@app.route('/delete/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def delete(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('删除数据成功')
    return redirect(url_for('index'))

@app.route('/edit/<int:movie_id>', methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(title) > 20 or len(year) > 4:
            flash('输入错误')
            return redirect(url_for('edit'), movie = movie)
        
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('数据编辑成功')
        return redirect(url_for('index'))
    return render_template('edit.html', movie = movie)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('输入错误')
            return redirect(url_for('login'))
        user = User.query.first()
        print(user.username)
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功')
            return redirect(url_for('index'))
        flash('用户名密码错误')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('退出')
    return redirect('/index')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('输入非法')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('设置成功')
    
        return redirect(url_for('index'))
    return render_template('settings.html')    