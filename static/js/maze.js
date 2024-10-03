let startPoint = null;
let endPoint = null;
// start and end would be a an object with row and column properties
let solutions = [];
let solutionIndex = -1;

document.addEventListener('DOMContentLoaded', () => {
    renderMaze();
    listMazes();
    populateSolutionDropdown();
});

// Update the maze in the maze-container element
function renderMaze() {
    fetch('/rendermaze')
    .then(response => response.json())
    .then(data => {
        const container = document.querySelector('.maze-container');
        const mazeData = data.maze;
        const mazeElement = document.createElement('div');
        mazeElement.classList.add('maze');
    
        for (let row = 0; row < mazeData.length; row++) {
            const rowElement = document.createElement('div');
            rowElement.classList.add('maze-line');
    
            for (let column = 0; column < mazeData[row].length; column++) {
                const cell = mazeData[row][column];
                const cellElement = document.createElement('div');
                cellElement.classList.add('cell');
                if (cell.up) cellElement.classList.add('up');
                if (cell.down) cellElement.classList.add('down');
                if (cell.left) cellElement.classList.add('left');
                if (cell.right) cellElement.classList.add('right');
    
                if (cell.visited) {
                    const pathElement = document.createElement('div');
                    pathElement.classList.add('path');
                    cellElement.appendChild(pathElement);
                }

                // Check if the current cell is part of the solution
                // If it is, add a correspoding path element to the cell
                // depending of the direction based on the previous and next cells
                if (solutionIndex > -1) {
                    currentCellIndex = solutions[solutionIndex].slice(1, -1)
                        .findIndex(cell => cell[0] === row && cell[1] === column) + 1;
                        // we add 1 because the first cell is not part of the solution
                    console.log(currentCellIndex); 
                    if (currentCellIndex > 0) { // we skip the first cell
                        // here we add 2 path elements to the cell
                        // one for the previous cell and one for the next cell
                        // this is to create the illusion of a continuous path
                        const previousPathElement = document.createElement('div');
                        previousPathElement.classList.add('path');
                        previousPathElement.classList.add('previous-path');
                        const nextPathElement = document.createElement('div');
                        nextPathElement.classList.add('path');
                        nextPathElement.classList.add('next-path');

                        const previousCell = solutions[solutionIndex][currentCellIndex - 1];
                        const nextCell = solutions[solutionIndex][currentCellIndex + 1];

                        if (previousCell[0] === row && previousCell[1] === column - 1) {
                            previousPathElement.classList.add('right-path');
                        } else if (previousCell[0] === row && previousCell[1] === column + 1) {
                            previousPathElement.classList.add('left-path');
                        } else if (previousCell[0] === row - 1 && previousCell[1] === column) {
                            previousPathElement.classList.add('up-path');
                        } else if (previousCell[0] === row + 1 && previousCell[1] === column) {
                            previousPathElement.classList.add('down-path');
                        }

                        if (nextCell[0] === row && nextCell[1] === column - 1) {
                            nextPathElement.classList.add('right-path');
                        } else if (nextCell[0] === row && nextCell[1] === column + 1) {
                            nextPathElement.classList.add('left-path');
                        } else if (nextCell[0] === row - 1 && nextCell[1] === column) {
                            nextPathElement.classList.add('up-path');
                        } else if (nextCell[0] === row + 1 && nextCell[1] === column) {
                            nextPathElement.classList.add('down-path');
                        }

                        cellElement.appendChild(previousPathElement);
                        cellElement.appendChild(nextPathElement);
                    }
                }

                if (startPoint && startPoint.column === column && startPoint.row === row) {
                    const startElement = document.createElement('div');
                    startElement.classList.add('start');
                    cellElement.appendChild(startElement);
                }

                if (endPoint && endPoint.column === column && endPoint.row === row) {
                    const endElement = document.createElement('div');
                    endElement.classList.add('end');
                    cellElement.appendChild(endElement);
                }

                cellElement.addEventListener('click', (event) => handleCellClick(event, column, row));
    
                rowElement.appendChild(cellElement);
            }
    
            mazeElement.appendChild(rowElement);
        }
    
        container.innerHTML = '';
        container.appendChild(mazeElement);
    });
}

function generateMaze() {
    let size = document.getElementById('maze-size').value;
    fetch('/generatemaze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ size: size })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            clearSolutions();
            renderMaze();
        } else {
            alert(data.message);
            document.getElementById('maze-size').value = '';
            document.getElementById('maze-size').focus();
        }
    });
}

function handleCellClick(event, x, y) {
    showMenu(event.clientX, event.clientY, x, y);
}

function showMenu(mouseX, mouseY, cellX, cellY) {
    const existingMenu = document.querySelector('.menu');
    if (existingMenu) {
        document.body.removeChild(existingMenu);
    }

    const menu = document.createElement('div');
    menu.classList.add('menu');
    menu.style.left = `${mouseX}px`;
    menu.style.top = `${mouseY}px`;

    const startButton = document.createElement('button');
    startButton.textContent = 'Set as Start';
    startButton.addEventListener('click', () => {
        startPoint = { row: cellY, column: cellX };
        document.body.removeChild(menu);
        clearSolutions();
        renderMaze();
    });

    const endButton = document.createElement('button');
    endButton.textContent = 'Set as End';
    endButton.addEventListener('click', () => {
        endPoint = { row: cellY, column: cellX };
        document.body.removeChild(menu);
        clearSolutions();
        renderMaze();
    });

    menu.appendChild(startButton);
    menu.appendChild(endButton);
    document.body.appendChild(menu);
}

function solveMaze() {
    if (!startPoint || !endPoint) {
        alert('Please set both start and end points.');
        return;
    }
    clearSolutions();
    fetch('/solvebybruteforce', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ start: startPoint, end: endPoint })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            solutions = data.solutions;
            solutionIndex = 0;
            populateSolutionDropdown();
            showSolution();
        } else {
            alert(data.message);
        }
    });
}

function populateSolutionDropdown() {
    const solutionDropdown = document.getElementById('solution-dropdown');
    solutionDropdown.innerHTML = '<option value="-1">No solution</option>';
    if (solutions.length === 0) {
        solutionDropdown.disabled = true;
    }
    solutionDropdown.disabled = false;
    for (let i = 0; i < solutions.length; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = `Solution ${i + 1}`;
        solutionDropdown.appendChild(option);
    }
    solutionDropdown.value = solutionIndex;
}

function showSolution() {
    const solutionDropdown = document.getElementById('solution-dropdown');
    solutionIndex = parseInt(solutionDropdown.value);
    renderMaze();
}

function saveMaze() {
    const mazeName = document.getElementById('maze-name').value;
    fetch('/savemaze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: mazeName })
        // gracias Dios por haberme hecho trabajar en una REST API este semestre
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            listMazes();
        } else {
            alert(data.message);
            document.getElementById('maze-name').value = '';
            document.getElementById('maze-name').focus();
        }
    });
}

function loadMaze() {
    const mazeName = document.getElementById('maze-name').value;
    fetch('/loadmaze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: mazeName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            renderMaze();
        } else {
            alert(data.message);
        }
    });
}

function listMazes() {
    fetch('/listmazes')
    .then(response => response.json())
    .then(data => {
        const savedMazesList = document.getElementById('saved-mazes');
        savedMazesList.innerHTML = '';
        for (let i = 0; i < data.mazes.length; i++) {
            const maze = data.mazes[i];
            const buttonItem = document.createElement('button');
            buttonItem.textContent = maze;
            buttonItem.classList.add('saved-maze-button');
            buttonItem.onclick = () => {
                document.getElementById('maze-name').value = maze;
                loadMaze();
                closeLoadModal();
            };
            savedMazesList.appendChild(buttonItem);
        }
    });
}

function clearSolutions() {
    solutionIndex = -1;
    renderMaze();
    solutions = [];
    populateSolutionDropdown();
}

function openLoadModal() {
    document.getElementById('load-modal').style.display = 'block';
    listMazes();
}

function closeLoadModal() {
    document.getElementById('load-modal').style.display = 'none';
}

// Close the modal when the user clicks outside of it
window.onclick = function(event) {
    const modal = document.getElementById('load-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}