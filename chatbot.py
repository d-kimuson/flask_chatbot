from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np


def rundom_message():
    messages = [  # 返信用
        "うぇーい",
        "ひょええ",
        "ぷえええ",
    ]
    return np.random.choice(messages)


app = Flask(__name__)


@app.route('/')
def index():
    title = "ようこそ"
    message = "名前を入力してね"
    return render_template("index.html",
                           message=message,
                           title=title)


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        name = request.form['name']
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


if __name__ == '__main__':
    # app.debug = True  # 本番環境ではコメントアウトする
    app.secret_key = ''
    app.run(host='0.0.0.0')
