from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Game {self.game}>'

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    games = Game.query.order_by(Game.date_added.desc()).all()
    return render_template('index.html', games=games)

@app.route('/add', methods=['POST'])
def add_game():
    game_name = request.form.get('game')
    game_year = request.form.get('year')
    
    if game_name and game_year:
        new_game = Game(game=game_name, year=int(game_year))
        db.session.add(new_game)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_game(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)