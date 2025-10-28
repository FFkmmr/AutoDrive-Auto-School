const carousel = document.querySelector('.carousel');
const group = carousel.querySelector('.group');

// получаем ширину блока и карусели
const groupWidth = group.offsetWidth;
const carouselWidth = carousel.offsetWidth;

// считаем, сколько блоков нужно добавить
const blocksNeeded = Math.ceil(carouselWidth / groupWidth) + 1;

for (let i = 0; i < blocksNeeded; i++) {
  const clone = group.cloneNode(true);
  clone.setAttribute('aria-hidden', 'true');
  carousel.appendChild(clone);
}
