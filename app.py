from flask import Flask, render_template, request, redirect, url_for
import random
from src.Maze import Maze

# FOR TESTING PURPOSES!!

# this class is only for testing!!, not the final version, it can be changed :)
# for it to be rendered in the html it just needs to have the up, down, left and right attributes
# it works by errasing the walls when one of the attributes is None
# just be sure to pass a matrix of cells to the reder_template function

# generate random maze
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

    # print formated maze
    for i in range(size):
        for j in range(size):
            print(f'[{i}][{j}]', end=' ')
            if maze[i][j].up is not None:
                print('U', end=' ')
            if maze[i][j].down is not None:
                print('D', end=' ')
            if maze[i][j].left is not None:
                print('L', end=' ')
            if maze[i][j].right is not None:
                print('R', end=' ')
        print('\n')

    return maze


# THE REAL DEAL

# we need this to be global so we can access it from the render_maze function
# that the client calls repeatedly
app = Flask(__name__, template_folder='templates')
maze = create_maze(10)
testSolution = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                (1, 4), (2, 4), (2, 3), (2, 2), (3, 2), (4, 2)]

@app.route('/rendermaze', methods=['GET', 'POST'])
def render_maze():
    return render_template('maze.html', maze=maze, solution=testSolution)

@app.route('/')
def index():
    # the solution is a list of tuples, each tuple is a coordinate of the maze (x, y)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
