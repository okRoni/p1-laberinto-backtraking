from flask import Flask, render_template, request, redirect, url_for
import random
import threading
import time
from src.Maze import Maze

# FOR TESTING PURPOSES!!

# this class is only for testing!!, not the final version, it can be changed :)
# for it to be rendered in the html it just needs to have the up, down, left and right attributes
# it works by errasing the walls when one of the attributes is None
# just be sure to pass a matrix of cells to the reder_template function


class cell:
    def __init__(self, up=None, down=None, left=None, right=None):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def connectUp(self, section):
        self.up = section
        section.down = self

    def connectDown(self, section):
        self.down = section
        section.up = self

    def connectLeft(self, section):
        self.left = section
        section.right = self

    def connectRight(self, section):
        self.right = section
        section.left = self

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

app = Flask(__name__, template_folder='templates')
maze = create_maze(5)
testSolution = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                (1, 4), (2, 4), (2, 3), (2, 2), (3, 2), (4, 2)]

def update_solution():
    global testSolution
    while True:
        # Update the testSolution with new coordinates
        testSolution = [(random.randint(0, 4), random.randint(0, 4)) for _ in range(10)]
        time.sleep(0.016)  # Wait for 5 seconds before updating again

@app.route('/rendermaze', methods=['GET', 'POST'])
def render_maze():
    return render_template('maze.html', maze=maze, solution=testSolution)

@app.route('/')
def index():
    # the solution is a list of tuples, each tuple is a coordinate of the maze (x, y)
    return render_template('index.html')

if __name__ == '__main__':
    thread = threading.Thread(target=update_solution)
    thread.daemon = True
    thread.start()
    app.run(debug=True)

