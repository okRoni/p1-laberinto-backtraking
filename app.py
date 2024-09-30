from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import os
from src.Maze import Maze

app = Flask(__name__, template_folder='templates')

def create_maze(size):
    maze: Maze = Maze(size=size, name='test')
    for i in range(size):
        for j in range(size):
            if i > 0 and random.randint(0, 1) == 0:
                maze[i][j].connect_up(maze[i-1][j])
            if i < size-1 and random.randint(0, 1) == 0:
                maze[i][j].connect_down(maze[i+1][j])
            if j > 0 and random.randint(0, 1) == 0:
                maze[i][j].connect_left(maze[i][j-1])
            if j < size-1 and random.randint(0, 1) == 0:
                maze[i][j].connect_right(maze[i][j+1])
    return maze

maze = create_maze(12)
# test in (i, j) format, where i is the row and j is the column.
testSolution = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                (1, 4), (2, 4), (2, 3), (2, 2), (3, 2), (4, 2)]
for i in range(len(testSolution)):
    maze[testSolution[i][0]][testSolution[i][1]].visited = True

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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)