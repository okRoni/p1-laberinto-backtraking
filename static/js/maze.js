document.addEventListener('DOMContentLoaded', renderMaze);

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