from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import os
from src.Maze import Maze
from src.pathfinding import get_routes

app = Flask(__name__, template_folder='templates')

maze : Maze = Maze(15, 'maze')
routes : list[list[tuple[int, int]]] = []
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
    if maze_size is None or not maze_size.isdigit():
        return jsonify({'status': 'error', 'message': 'Invalid maze size.'})
    maze_size = int(maze_size)
    if maze_size < 5 or maze_size > 50:
        return jsonify({'status': 'error', 'message': 'Maze size must be between 5 and 50.'})
    maze = Maze(int(maze_size), 'maze')
    maze.generate_maze()
    return jsonify({'status': 'success', 'message': 'Maze generated successfully.'})

@app.route('/unvisitall', methods=['POST'])
def unvisit_all():
    global maze
    maze.unvisit_all()
    return jsonify({'status': 'success', 'message': 'All cells unvisited.'})

@app.route('/solvemaze', methods=['POST'])
def solve_by_brute_force():
    global maze
    global routes
    global states
    maze.unvisit_all()
    start = (request.json.get('start')['row'], request.json.get('start')['column'])
    end = (request.json.get('end')['row'], request.json.get('end')['column'])
    algorithm = request.json.get('algorithm')
    if start is None or end is None:
        return jsonify({'status': 'error', 'message': 'Invalid start or end cell.'})
    if algorithm == 'a-star':
        result = get_routes(maze, start, end, True)
        routes = result[0]
        states = result[1]
    else:
        result = get_routes(maze, start, end, False)
        routes = result[0]
        states = result[1]
    if routes == []:
        return jsonify({'status': 'error', 'message': 'No routes found.'})
    return jsonify({'status': 'success', 'solutions': routes, 'states': states})


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)