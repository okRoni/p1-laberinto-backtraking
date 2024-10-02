let startPoint = null;
let endPoint = null;
// it would be a an object with row and column properties

document.addEventListener('DOMContentLoaded', () => {
    renderMaze();
    listMazes();
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
    try {
        size = parseInt(size);
    } catch (e) {
        alert('El tamaño del laberinto debe ser un número');
        return;
    }
    if (size < 3 || size > 50) {
        alert('El tamaño del laberinto debe estar entre 3 y 50');
        return;
    }
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
            renderMaze();
        } else {
            alert(data.message);
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
        unvisitALl();
        renderMaze();
    });

    const endButton = document.createElement('button');
    endButton.textContent = 'Set as End';
    endButton.addEventListener('click', () => {
        endPoint = { row: cellY, column: cellX };
        document.body.removeChild(menu);
        unvisitALl();
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
    unvisitALl();
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
            renderMaze();
        } else {
            alert(data.message);
        }
    });
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

function unvisitALl() {
    fetch('/unvisitall', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
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