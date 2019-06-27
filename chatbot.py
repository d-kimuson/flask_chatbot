from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import database as db


def rundom_message():
    messages = [  # 返信用
        "うぇーい",
        "ひょええ",
        "ぷえええ",
    ]
    return np.random.choice(messages)


app = Flask(__name__)
app.secret_key = 'hoigeowooa'
db_controller = db.DBController()

"""
session['state']
- user
- visitor
- login_failed
"""


@app.route('/')
def index():
    title = "ようこそ"
    if 'state' not in session.keys():
        update_state(session, is_login=False)
    return render_template("index.html", title=title)


@app.route('/go_chat', methods=['GET', 'POST'])
def go_chat():
    if request.method == 'POST':
        name = session['name']
        if name == "":
            name = "名無し"
        session['name'] = name
        session['message_log'] = [
            {"author": "Koshikawa", "content": f"こんにちは {name} さん"},
            {"author": "Koshikawa", "content": "僕の名前はこしかわだよ!"},
        ]
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('index'))


@app.route('/change_name', methods=['GET', 'POST'])
def change_name():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name
        db_controller.update_user(
            session['mail'],
            name=session['name']
            )
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/chat/')
def chat():
    title = "Chat"
    return render_template(f"chat.html",
                           name=session['name'],
                           messages=session['message_log'],
                           title=title)


@app.route('/message_post', methods=['GET', 'POST'])
def message_post():
    if request.method == 'POST':
        message = request.form['message']
        author = session['name']
        message_log = session['message_log']
        message_log.append({  # postされたメッセージをログへ追加
            "author": author,
            "content": message
            })
        message_log.append({  # メッセージへの返信をログへ追加
            "author": "Koshikawa",
            "content": rundom_message()
             })
        session['message_log'] = message_log
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('index'))


@app.route('/make_account/')
def make_account():
    title = "アカウント登録"
    return render_template(f"make_account.html", title=title)


@app.route('/make', methods=['GET', 'POST'])
def make():
    if request.method == 'POST':
        mail = request.form['mail']
        passwd = request.form['passwd']
        result = db_controller.add_user(mail=mail, password=passwd)
        if result:
            update_state(session, is_login=True, mail=mail)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/login_page/')
def login_page():
    title = "ログイン"
    return render_template(f"login.html", title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        passwd = request.form['passwd']
        if db_controller.auth(mail, passwd):
            print("login!!")
            update_state(session, is_login=True, mail=mail)
            print(session)
            return redirect(url_for('index'))
        else:
            session['state'] = "login_failed"
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    update_state(session, is_login=False)
    return redirect(url_for('index'))


def update_state(session, is_login, mail=None):
    if 'state' not in session.keys():
        session['state'] = "visitor"
    if 'mail' not in session.keys():
        session['mail'] = None
    if is_login:
        session['state'] = "user"
        session['mail'] = mail
    else:
        session['state'] = "visitor"
        session['mail'] = None


if __name__ == '__main__':
    app.debug = True  # 本番環境ではコメントアウトする
    app.run(host='0.0.0.0')
