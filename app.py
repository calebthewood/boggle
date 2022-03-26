from operator import is_
from pickle import FALSE
from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}

@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})

@app.post("/api/score-word")
def score_word():
    """Score word and return JSON: {result: ...}"""

    response = request.json
    word_input = response["word-input"]
    game_id = response["gameId"]

    game_instance = games[game_id]

    if game_instance.is_word_in_word_list(word_input) is False:
        return jsonify({"result":"not-word"})
    if game_instance.check_word_on_board(word_input) is False:
        return jsonify({"result":"not-on-board"})
    return jsonify({"result":"ok"})


