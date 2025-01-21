import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

import omikuji

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = "your_secret_key"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


with app.app_context():
    db.create_all()


### タスクを表示する ###
@app.route("/", methods=["GET", "POST"])
def home():
    todo_list = Todo.query.all()
    fortune_result = session.get("fortune_result", "")
    fortune_advice = session.get("fortune_advice", "")
    # 取得したTodoリストを"index.html"テンプレートに渡し、ウェブページとして表示
    return render_template(
        "./index.html", todo_list=todo_list, fortune_result=fortune_result, fortune_advice=fortune_advice
    )


### タスク追加 ###
@app.route("/add", methods=["POST"])
def add():
    # ユーザーから送信されたフォームデータからタイトルを取得
    title = request.form.get("title")
    # 新しいTodoオブジェクトを作成
    new_todo = Todo(title=title)
    # 新しいTodoをデータベースセッションに追加
    db.session.add(new_todo)
    # 変更をデータベースにコミット
    db.session.commit()
    # タスク追加後、ホームページにリダイレクト
    return redirect(url_for("home"))


### タスク削除 ###
@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    # URLから渡されたIDに基づいて、該当するTodoをデータベースから取得
    todo = Todo.query.filter_by(id=todo_id).first()
    # 取得したTodoをデータベースセッションから削除
    db.session.delete(todo)
    # 変更をデータベースにコミット
    db.session.commit()
    # タスク削除後、ホームページにリダイレクト
    return redirect(url_for("home"))


@app.route("/example", methods=["POST"])
def example():
    fortune_result = ""
    fortune_advice = ""

    if request.method == "POST":
        fortune = omikuji.draw()
        fortune_result = fortune.result.value
        fortune_advice = fortune.advice
        session["fortune_result"] = fortune_result
        session["fortune_advice"] = fortune_advice
    else:
        fortune_result = ""
        fortune_advice = ""

    todos = Todo.query.all()
    return render_template("index.html", todo_list=todos, fortune_result=fortune_result, fortune_advice=fortune_advice)


if __name__ == "__main__":
    app.run(debug=True)


def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # ここでは、例としてタイトルタグを取得します
    title = soup.find("title").get_text()
    return title


@app.route("/scrape", methods=["GET"])
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        title = scrape_website(url)
        return jsonify({"title": title})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
