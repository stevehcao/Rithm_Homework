from flask import Flask, render_template, request, url_for, redirect
from flask_modus import Modus

app = Flask(__name__)
Modus(app)


class Game:
    count = 1

    def __init__(self, name, system, rating):
        self.name = name
        self.system = system
        self.rating = rating
        self.id = Game.count
        Game.count += 1


zelda = Game('Zelda: Breath of the Wild', 'Switch', 97)
horizon = Game('Horizon Zero Dawn', 'PS4', 89)
mario = Game('Super Mario Odyssey', 'Switch', 97)
injustice = Game('Injustice 2', 'Xbox One', 89)

games = [zelda, horizon, mario, injustice]


# home page
@app.route('/')
def home():
    return render_template('home.html')


# route to show a list of all the games
@app.route('/games')
def index():
    return render_template('index.html', games=games)


# route to show form to add a game
@app.route('/games/new')
def new():
    return render_template('new.html')


# why is it routing games?
# can this be anything since it's only purpose is to append  a new game?
@app.route('/games', methods=['POST'])
def create():
    new_game = Game(
        request.values.get('name'), request.values.get('system'),
        request.values.get('rating'))
    games.append(new_game)
    return redirect(url_for('index'))


@app.route('/games/<int:id>', methods=['GET'])
def show(id):
    # need to grab id somehow to add to route
    found_game = [game for game in games if id == game.id][0]
    return render_template('show.html', game=found_game)


@app.route('/games/<int:id>', methods=["DELETE"])
def destroy(id):
    # need to grab id again
    # this time we will remove from list
    # the button on the show.html will activate this function
    # this function will then grab the id of the game from the url and then run the function
    found_game = [game for game in games if id == game.id][0]
    games.remove(found_game)
    return redirect(url_for('index'))


# form to edit
@app.route('/games/<int:id>/edit', methods=['GET'])
def edit(id):
    found_game = [game for game in games if id == game.id][0]
    return render_template('edit.html', game=found_game)


@app.route("/games/<int:id>", methods=["PATCH"])
def update(id):
    found_game = [game for game in games if game.id == id][0]
    found_game.name = request.values.get('name')
    found_game.system = request.values.get('system')
    found_game.rating = request.values.get('rating')
    return redirect(url_for('show', id=found_game.id))
