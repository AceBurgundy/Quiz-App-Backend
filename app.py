from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer)

    def __init__(self, name, score=0):
        self.name = name
        self.score = score

@app.post('/add_player')
def add_player():
    data = request.get_json()
    name = data.get('name')

    player = Player.query.filter_by(name=name).first()
    if player:
        return jsonify({'status': 'error', 'message': 'Player name already exists.'})

    player = Player(name)
    db.session.add(player)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Player added successfully.'})

@app.route('/get_players', methods=['GET'])
def get_players():
    players = Player.query.all()

    if not players:
        return jsonify({'status': 'error', 'message':'No players yet'})
    
    result = []
    for player in players:
        result.append({'name': player.name, 'score': player.score})
    return jsonify({'status': 'success', 'players': result})

@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.get_json()
    name = data.get('name')
    score = data.get('score')

    if not name:
        return jsonify({'status': 'error', 'message': 'Name is required.'})

    player = Player.query.filter_by(name=name).first()
    if not player:
        return jsonify({'status': 'error', 'message': 'Player not found.'})

    if score is not None:
        player.score = score

    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Player score updated successfully.'})

@app.route('/delete_players', methods=['POST'])
def delete_players():
    Player.query.delete()
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'All players deleted successfully.'})

@app.post('/delete_player')
def delete_player():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'status': 'error', 'message': 'Name is required.'})

    player = Player.query.filter_by(name=name).first()
    if not player:
        return jsonify({'status': 'error', 'message': 'No records yet.'})

    db.session.delete(player)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Player deleted successfully.'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
