from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import os
from src.Maze import Maze
from src.pathfinding import get_routes_bt

app = Flask(__name__, template_folder='templates')

maze : Maze = Maze(15, 'maze')
maze.generate_maze()

@app.route('/rendermaze', methods=['GET'])
def render_maze():
    maze_data = [[{
        'up': cell.up is not None,
        'down': cell.down is not None,
        'left': cell.left is not None,
        'right': cell.right is not None,
        'visited': cell.visited
    } for cell in row] for row in maze.cell_matrix]
    return jsonify({'maze': maze_data})

@app.route('/savemaze', methods=['POST'])
def save_maze():
    maze_name = request.json.get('name')
    if maze_name:
        maze.name = maze_name
        maze.store()
        return jsonify({'status': 'success', 'message': 'Maze saved successfully.'})
    return jsonify({'status': 'error', 'message': 'Error saving the maze.'})

@app.route('/loadmaze', methods=['POST'])
def load_maze():
    maze_name = request.json.get('name')
    if maze_name:
        filepath = f'src/mazes/{maze_name}.txt'
        maze.load(filepath)
        return jsonify({'status': 'success', 'message': 'Maze loaded successfully.'})
    return jsonify({'status': 'error', 'message': 'Error loading the maze.'})

@app.route('/listmazes', methods=['GET'])
def list_mazes():
    mazes_dir = 'src/mazes'
    mazes = [f.split('.')[0] for f in os.listdir(mazes_dir) if f.endswith('.txt')]
    return jsonify({'mazes': mazes})

@app.route('/generatemaze', methods=['POST'])
def generate_maze():
    global maze
    maze_size = request.json.get('size')
    maze = Maze(int(maze_size), 'maze')
    maze.generate_maze()
    if maze_size is None or int(maze_size) < 1:
        return jsonify({'status': 'error', 'message': 'Invalid maze size.'})
    print(*get_routes_bt(maze, (0, 0), (maze_size - 1, maze_size - 1)), sep='\n')
    return jsonify({'status': 'success', 'message': 'Maze generated successfully.'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)