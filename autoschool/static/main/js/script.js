const line = document.querySelector('.line');

// Клонируем все элементы, чтобы создать бесконечность
const clones = Array.from(line.children).map(img => img.cloneNode(true));
clones.forEach(clone => line.appendChild(clone));

let speed = 1; // скорость прокрутки в px за кадр
let pos = 0;

function animate() {
    pos -= speed;
    // Когда первая половина пройдена, сбрасываем позицию
    if (pos <= -line.scrollWidth / 2) {
        pos = 0;
    }
    line.style.transform = `translateX(${pos}px)`;
    requestAnimationFrame(animate);
}

animate();
