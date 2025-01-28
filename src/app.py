import random

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

import omikuji

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = "your_secret_key"
db = SQLAlchemy(app)

board = [["" for _ in range(8)] for _ in range(8)]
board[3][3] = board[4][4] = "W"
board[3][4] = board[4][3] = "B"
current_turn = "B"

directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


with app.app_context():
    db.create_all()


def is_valid_move(board, x, y, player):
    if board[y][x] != "":
        return False

    opponent = "W" if player == "B" else "B"
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == opponent:
            while 0 <= nx < 8 and 0 <= ny < 8:
                nx += dx
                ny += dy
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                if board[ny][nx] == "":
                    break
                if board[ny][nx] == player:
                    return True
    return False


def get_valid_moves(board, player):
    valid_moves = []
    for y in range(8):
        for x in range(8):
            if is_valid_move(board, x, y, player):
                valid_moves.append((x, y))
    return valid_moves


def make_move(board, x, y, player):
    board[y][x] = player
    opponent = "W" if player == "B" else "B"
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        to_flip = []
        while 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == opponent:
            to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == player:
            for fx, fy in to_flip:
                board[fy][fx] = player


def ai_move():
    global current_turn
    valid_moves = get_valid_moves(board, current_turn)
    if valid_moves:
        x, y = random.choice(valid_moves)
        make_move(board, x, y, current_turn)
        current_turn = "W" if current_turn == "B" else "B"


@app.route("/")
def index():
    valid_moves = get_valid_moves(board, current_turn)
    return render_template("index.html", board=board, current_turn=current_turn, valid_moves=valid_moves)


@app.route("/move", methods=["POST"])
def move():
    global current_turn
    x = int(request.form["x"])
    y = int(request.form["y"])

    if is_valid_move(board, x, y, current_turn):
        make_move(board, x, y, current_turn)
        current_turn = "W" if current_turn == "B" else "B"
        if current_turn == "W":
            ai_move()
    return jsonify(success=True)


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


if __name__ == "__main__":
    app.run(debug=True)
