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
        const solution = data.solution;
        const mazeElement = document.createElement('div');
        mazeElement.classList.add('maze');
    
        for (let y = 0; y < mazeData.length; y++) {
            const rowElement = document.createElement('div');
            rowElement.classList.add('maze-line');
    
            for (let x = 0; x < mazeData[y].length; x++) {
                const cell = mazeData[y][x];
                const cellElement = document.createElement('div');
                cellElement.classList.add('cell');
                if (cell.up) cellElement.classList.add('up');
                if (cell.down) cellElement.classList.add('down');
                if (cell.left) cellElement.classList.add('left');
                if (cell.right) cellElement.classList.add('right');
    
                if (solution.some(([sx, sy]) => sx === x && sy === y)) {
                    const pathElement = document.createElement('div');
                    pathElement.classList.add('path');
                    cellElement.appendChild(pathElement);
                }
    
                rowElement.appendChild(cellElement);
            }
    
            mazeElement.appendChild(rowElement);
        }
    
        container.innerHTML = '';
        container.appendChild(mazeElement);
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