from flask import Flask, render_template, request, redirect, url_for
import random


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
    maze = [[cell() for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            if i > 0 and random.randint(0, 1) == 0:
                maze[i][j].connectUp(maze[i-1][j])
            if i < size-1 and random.randint(0, 1) == 0:
                maze[i][j].connectDown(maze[i+1][j])
            if j > 0 and random.randint(0, 1) == 0:
                maze[i][j].connectLeft(maze[i][j-1])
            if j < size-1 and random.randint(0, 1) == 0:
                maze[i][j].connectRight(maze[i][j+1])

    # print formated maze
    for i in range(size):
        for j in range(size):
            print(f'[{i}][{j}]', end=' ')
            if maze[i][j].up != None:
                print('U', end=' ')
            if maze[i][j].down != None:
                print('D', end=' ')
            if maze[i][j].left != None:
                print('L', end=' ')
            if maze[i][j].right != None:
                print('R', end=' ')
        print('\n')

    return maze


## THE REAL DEAL

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    maze = create_maze(5)
    testSolution = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (2, 3), (2, 2), (3, 2), (4, 2)]
    # the solution is a list of tuples, each tuple is a coordinate of the maze (x, y)
    return render_template('index.html', maze=maze, solution=testSolution)

if __name__ == '__main__':
    app.run(debug=True)