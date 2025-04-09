from flask import Flask, render_template_string, request
from db import get_game, insert_game

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello world, welcome to Railway!'

@app.route('/upload', methods=['POST'])
def upload_game():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return 'No file part in request', 400
    
    file = request.files['file']
    content = file.read().decode('utf-8')

    # TODO: custom title
    game_id = insert_game('test', content)
    # print(f'http://localhost:8000/game/{game_id}')
    return game_id

@app.route('/game/<game_id>')
def serve_game(game_id):
    game = get_game(game_id)
    return render_template_string(game['code'])

if __name__ == '__main__':
    app.run(debug=True)