from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


### タスクを表示する ###
@app.route("/", methods=["GET", "POST"])
def home():
    # データベースから全てのTodoレコードを取得
    todo_list = Todo.query.all()
    # 取得したTodoリストを"index.html"テンプレートに渡し、ウェブページとして表示
    return render_template("index.html", todo_list=todo_list)

<<<<<<< HEAD
=======
    Returns:
        str: レンダリング結果
    """
    # 明日の日付（曜日表示付き）
    DAY_NAME = "月火水木金土日つｊ"
    tomorrow_dt = datetime.now() + timedelta(days=1)
    tomorrow_dt_str = f"{tomorrow_dt.strftime('%Y/%m/%d')}({DAY_NAME[tomorrow_dt.weekday()]})"
>>>>>>> e4e7eeadce2ce59483296a722c2f9266d71d08c3

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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

