let startPoint = null;
let endPoint = null;
// start and end would be a an object with row and column properties
let solutions = [];
let solutionIndex = -1;
let states = [];
let maze = [];
let inProcess = false;
let timeoutIds = []; // to stop the process later!

document.addEventListener('DOMContentLoaded', () => {
    fetchAndUpdateMaze();
    listMazes();
    populateSolutionDropdown();
    document.getElementById('process-button').disabled = true;
});

/**
 * Fetch the maze from the server and update the maze variable
 */
function fetchAndUpdateMaze() {
    fetch('/rendermaze')
    .then(response => response.json())
    .then(data => {
        maze = data.maze;
        renderMaze();
        if (solutions.length = 0) {
            document.getElementById('process-button').disabled = true;
        }
    });
}

/**
 * Render the maze on the screen
 * @param {Array} paths - The paths to render (default to solutions)
 * @param {Number} pathIndex - The index of the path to render (default to solutionIndex)
 */
function renderMaze(paths = solutions, pathIndex = solutionIndex) {
    const container = document.querySelector('.maze-container');
    const mazeElement = document.createElement('div');
    mazeElement.classList.add('maze');

    for (let row = 0; row < maze.length; row++) {
        const rowElement = document.createElement('div');
        rowElement.classList.add('maze-line');

        for (let column = 0; column < maze[row].length; column++) {
            const cell = maze[row][column];
            const cellElement = document.createElement('div');
            cellElement.classList.add('cell');
            if (cell.up) cellElement.classList.add('up');
            if (cell.down) cellElement.classList.add('down');
            if (cell.left) cellElement.classList.add('left');
            if (cell.right) cellElement.classList.add('right');

            // Check if the current cell is part of the path
            // If it is, add a correspoding path element to the cell
            // depending of the direction based on the previous and next cells
            if (pathIndex > -1) {
                currentCellIndex = paths[pathIndex].slice(1, -1)
                    .findIndex(cell => cell[0] === row && cell[1] === column) + 1;
                    // we add 1 because the first cell is not part of the solution
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

                    const previousCell = paths[pathIndex][currentCellIndex - 1];
                    const nextCell = paths[pathIndex][currentCellIndex + 1];

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
}

/**
 * Show the process of solving the maze
 * This function will render the maze at each step of the process
 * The steps are stored in the states variable
 */
function showProcess() {
    setAllImputsDisable(true);
    inProcess = true;
    const processButton = document.getElementById('process-button');
    processButton.disabled = false;
    delayMilliSeconds = 16;
    ChangeProcessButton();
    for (let i = 0; i < states.length; i++) {
        const timeoutId = setTimeout(() => {
            renderMaze(states, i);
        },i * delayMilliSeconds);
        timeoutIds.push(timeoutId);
    }
    // when the process is done:
    setTimeout(() => {
        finishProcess();
    }, states.length * delayMilliSeconds);
}

/**
 * Finish the process of solving the maze
 */
function finishProcess() {
    for (const timeoutId of timeoutIds) {
        clearTimeout(timeoutId);
    }
    timeoutIds = [];
    setAllImputsDisable(false);
    inProcess = false;
    renderMaze();
    ChangeProcessButton();
}

/**
 * Disable or enable all inputs in the page
 * @param {Boolean} value - True to disable all inputs, false to enable them
 */
function setAllImputsDisable(value) {
    const buttons = document.getElementsByTagName('button');
    for (let i = 0; i < buttons.length; i++) {
        console.log(buttons[i].textContent);
        buttons[i].disabled = value;
    }
    const dropdowns = document.getElementsByTagName('select');
    for (let i = 0; i < dropdowns.length; i++) {
        dropdowns[i].disabled = value;
    }
    const inputs = document.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].disabled = value;
    }
}

/**
 * Change the text of the process button
 */
function ChangeProcessButton() {
    const processButton = document.getElementById('process-button');
    if (inProcess) {
        processButton.textContent = 'Cancel';
    } else {
        processButton.textContent = 'Show steps';
    }
}

/**
 * Handle the click event of the process button
 */
function handleProcessButton() {
    if (inProcess) { // stop the process
        finishProcess();
    } else { // start the process
        showProcess();
    }
}

/**
 * Clear the start and end points
 */
function clearStartEnd() {
    startPoint = null;
    endPoint = null;
};


/**
 * Generate a new maze
 */
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
            clearStartEnd();
            clearSolutions();
            fetchAndUpdateMaze();
        } else {
            alert(data.message);
            document.getElementById('maze-size').value = '';
            document.getElementById('maze-size').focus();
        }
    });
}

/**
 * Handle the click event of a cell
 * @param {Event} event - The click event
 * @param {Number} x - The column of the cell
 * @param {Number} y - The row of the cell
 */
function handleCellClick(event, x, y) {
    if (inProcess) {
        return;
    }
    showMenu(event.clientX, event.clientY, x, y);
}

/**
 * Show the context menu to set the start or end point
 */
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

/**
 * Solve the maze using the selected algorithm
 */
function solveMaze() {
    if (!startPoint || !endPoint) {
        alert('Please set both start and end points.');
        return;
    }
    clearSolutions();
    setAllImputsDisable(true);
    inProcess = true;
    
    document.body.style.cursor = 'wait';

    fetch('/solvemaze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
        { 
            start: startPoint,
            end: endPoint,
            algorithm: document.getElementById('algorithm-dropdown').value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            solutions = data.solutions;
            solutionIndex = 0;
            states = data.states;
            populateSolutionDropdown();
            showSolution();
            document.getElementById('process-button').disabled = false;
        } else {
            alert(data.message);
        }
        setAllImputsDisable(false);
        
        document.body.style.cursor = 'default';
        inProcess = false;
    })
    .catch(error => {
        alert('An error occurred while solving the maze.');
        setAllImputsDisable(false);

        document.body.style.cursor = 'default';
        inProcess = false;
    });
}

/**
 * Populate the solution dropdown with the available solutions
 */
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

/**
 * Show the selected solution
 */
function showSolution() {
    const solutionDropdown = document.getElementById('solution-dropdown');
    solutionIndex = parseInt(solutionDropdown.value);
    renderMaze();
}

/**
 * saves the maze with the given name
 */
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

/**
 * load the maze with the given name
 */
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
            fetchAndUpdateMaze();
            clearSolutions();
            clearStartEnd();
            document.getElementById('process-button').disabled = true;
        } else {
            alert(data.message);
        }
    });
}

/**
 * fetch the list of saved mazes and update the saved mazes list
 */
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

/**
 * clear the solutions and the states
 */
function clearSolutions() {
    solutionIndex = -1;
    renderMaze();
    solutions = [];
    states = [];
    populateSolutionDropdown();
    document.getElementById('process-button').disabled = true;
}

/**
 * Open the load modal
 */
function openLoadModal() {
    document.getElementById('load-modal').style.display = 'block';
    listMazes();
}

/**
 * Close the load modal
 */
function closeLoadModal() {
    document.getElementById('load-modal').style.display = 'none';
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    const modal = document.getElementById('load-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}