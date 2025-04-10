from flask import Flask, render_template_string, request
from db import get_game, get_games, insert_game

app = Flask(__name__)

@app.route('/')
def index():
    games = get_games()

    games_code = ''
    for game in games:
        games_code += f'<li><a href="https://igrobuilder.up.railway.app/game/{game["id"]}">{game["title"]} by @{game["username"]}</a></li>'

    html = f'''
    <html>
        <head>
            <title>Recent Games</title>
        </head>
        <body>
            <h1>Recent Games</h1>
            <ul id="games">
                {games_code}
            </ul>
        </body>
    </html>
    '''

    return render_template_string(html)

@app.route('/upload', methods=['POST'])
def upload_game():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return 'No file part in request', 400
    
    file = request.files['file']
    content = file.read().decode('utf-8')

    title = request.form.get('title', 'Untitled Game')
    username = request.form.get('username', 'Anonymous')

    game_id = insert_game(title, content, username)
    return game_id

@app.route('/game/<game_id>')
def serve_game(game_id):
    game = get_game(game_id)
    return render_template_string(game['code'])

if __name__ == '__main__':
    app.run(debug=True)