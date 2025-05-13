const gameBox = document.getElementById("gameBox");
const scoreDisplay = document.getElementById("score");
let score = 0;

// Move box to a random position within the window
function moveBox() {
    const maxX = window.innerWidth - 60;
    const maxY = window.innerHeight - 60;
    const randomX = Math.floor(Math.random() * maxX);
    const randomY = Math.floor(Math.random() * maxY);

    gameBox.style.left = `${randomX}px`;
    gameBox.style.top = `${randomY}px`;
}

// Handle box click
gameBox.addEventListener("click", () => {
    score++;
    scoreDisplay.textContent = score;
    moveBox();
});

// Start position
moveBox();
