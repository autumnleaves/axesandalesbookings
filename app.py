
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
games = []
tables = set(range(1, 21))  # Assume 20 tables available

@app.route('/')
def index():
    return render_template_string('''
        <h1>Board Game Club</h1>
        <h2>Host a Game</h2>
        <form method="post" action="/host">
            Game Name: <input name="game"><br>
            Host Name: <input name="host"><br>
            Number of Players: <input name="players" type="number"><br>
            <input type="submit" value="Host Game">
        </form>
        <h2>Available Games</h2>
        {% for game in games %}
            <div>
                <strong>{{ game['game'] }}</strong> hosted by {{ game['host'] }} at Table {{ game['table'] }}<br>
                Players ({{ game['signed_up']|length }}/{{ game['players'] }}): 
                {% for p in game['signed_up'] %}
                    {{ p['name'] }}{% if p['new'] %} (New){% endif %},
                {% endfor %}
                <form method="post" action="/signup/{{ loop.index0 }}">
                    Your Name: <input name="name">
                    New to Game? <input type="checkbox" name="new">
                    <input type="submit" value="Sign Up">
                </form>
                <form method="post" action="/cancel/{{ loop.index0 }}">
                    <input type="submit" value="Cancel Game">
                </form>
            </div>
        {% endfor %}
    ''', games=games)

@app.route('/host', methods=['POST'])
def host():
    if tables:
        table = tables.pop()
        games.append({
            'game': request.form['game'],
            'host': request.form['host'],
            'players': int(request.form['players']),
            'table': table,
            'signed_up': []
        })
    return redirect(url_for('index'))

@app.route('/signup/<int:game_id>', methods=['POST'])
def signup(game_id):
    game = games[game_id]
    if len(game['signed_up']) < game['players']:
        game['signed_up'].append({
            'name': request.form['name'],
            'new': 'new' in request.form
        })
    return redirect(url_for('index'))

@app.route('/cancel/<int:game_id>', methods=['POST'])
def cancel(game_id):
    table = games[game_id]['table']
    tables.add(table)
    games.pop(game_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
