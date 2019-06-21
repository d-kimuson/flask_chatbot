from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)

message_log = []
name = ""


def rundom_message():
    messages = [  # 返信用メッセージリスト
        "うぇーい",
        "ひょええ",
        "ぷえええ",
    ]
    return np.random.choice(messages)


@app.route('/')
def index():
    title = "ようこそ"
    message = "名前を入力してね"
    return render_template("index.html",
                           message=message,
                           title=title)


@app.route('/post', methods=['GET', 'POST'])
def post():
    global name
    title = "こんにちは"
    if request.method == 'POST':
        name = request.form['name']
        return render_template(f"index.html",
                               name=name,
                               title=title)
    else:
        return redirect(url_for('index'))


@app.route('/message_post', methods=['GET', 'POST'])
def message_post():
    global message_log
    title = "こんにちは"
    if request.method == 'POST':
        message = request.form['message']
        author = name
        message_log.append({  # postされたメッセージをログへ追加
            "author": author,
            "content": message
            })
        message_log.append({  # メッセージへの返信をログへ追加
            "author": "Koshikawa",
            "content": rundom_message()
             })
        return render_template(f"index.html",
                               name=name,
                               message=message_log,
                               title=title)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0')
