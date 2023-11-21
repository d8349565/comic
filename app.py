from flask import Flask, render_template, redirect, session, request, url_for
import os
from datetime import timedelta
from model import *
from sqlalchemy import text

JSON_AS_ASCII = False

app = Flask(__name__)
app.static_url_path = '/static'
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=3)
app.JSON_AS_ASCII = False


def check_user(username, password):
    session_c = session_0()
    pw = session_c.query(User).filter_by(name=username).first()
    try:
        pw = pw.password
        return pw == password
    except:
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')


@app.before_request  # 执行所有装饰器都要执行当前装饰器(简洁版实现同样功能)
def login_required():
    if request.path in ['/login', '/register']:  # 如果登录的路由是注册和登录就返会none
        return None
    username = session.get('username')  # 获取用户登录信息
    if not username:  # 没有登录就自动跳转到登录页面去
        return redirect('/login')
    return None


@app.route('/')
def index():  # put application's code here
    session1 = session_0()
    res = session1.execute(text('''SELECT distinct p1.Comic_name, p1.Comic_cover, p2.title
FROM pic p1
JOIN (
    SELECT Comic_name, Comic_cover, MAX(Chapter_title) AS title
    FROM pic
    GROUP BY Comic_name, Comic_cover
) p2 ON p1.Comic_name = p2.Comic_name AND p1.Comic_cover = p2.Comic_cover;'''))
    data = res.fetchall()
    content = {}
    for i in data:
        content[i[0].strip()] = [i[1].strip(),i[2].strip()]
    session1.close()
    return render_template('index.html', content=content)


@app.route('/comic/<comic_name>/')
def comic_index(comic_name):
    session_c = session_0()
    sql = f'''select distinct Chapter_title from pic where Comic_name = '{comic_name}' order by Chapter_title'''
    res = session_c.execute(text(sql))
    data = res.fetchall()
    content = {comic_name: [i[0] for i in data]}
    try:
        history = session_c.query(user_history).filter(user_history.comic_name == comic_name, user_history.name == session['username']).all()[-1].title
    except:
        history =None
    session_c.close()
    return render_template('comic.html', content=content, history=history, comic_name=comic_name)


@app.route('/comic/<comic_name>/<title>')
def comic_detail(comic_name, title):
    session[comic_name] = title
    session_c = session_0()
    user_history01 = user_history(name=session['username'], comic_name=comic_name, title=title,
                                  createTime=datetime.now())
    session_c.add(user_history01)
    session_c.commit()
    # ---------------------------------------------------
    sql = f'''select distinct name,target_url from pic where Comic_name = '{comic_name}' and Chapter_title = '{title}' order by name'''
    res = session_c.execute(text(sql))
    data = res.fetchall()

    try:
        urls = [i[1].replace("baozicdn.com", "baozimh.com") for i in data]
    except:
        urls = [i[1] for i in data]
    sql = f'''select distinct Chapter_title from pic where Comic_name = '{comic_name}' order by Chapter_title'''
    res2 = session_c.execute(text(sql))
    data = res2.fetchall()
    titles = [i[0] for i in data]
    # ---------------------------------------------------
    session_c.close()
    num = titles.index(title)
    try:
        next_title = titles[num + 1]
    except:
        next_title = title + '?最后一页了，没有啦'

    return render_template('detail.html', comic_name=comic_name, urls=urls, next_title=next_title, title=title)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

# pyinstaller --onefile --add-data "static;static" --add-data "templates;templates" --add-data "comic.db;comic.db" app.py
# pyinstaller --onefile --add-data "static;static" --add-data "templates;templates" app.py
# 生成requirements.txt -> pip freeze > requirements.txt
