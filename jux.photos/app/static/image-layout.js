// This JS is not needed for the layout to work.
// All it does it add/remove images.

const add = document.querySelector('[data-add]');
const remove = document.querySelector('[data-remove]');
const card = document.querySelector('[data-card]');
const container = document.querySelector('[data-container]');
let number = 7;

add.addEventListener('click', () => {
  const addCard = card.cloneNode(true);
  const image = `url('https://source.unsplash.com/random/${Math.floor(Math.random() * 100)}')`;
  addCard.style.backgroundImage = image;
  addCard.innerHTML = number;
  container.appendChild(addCard);
  number++;
});

remove.addEventListener('click', () => {
  if (container.childElementCount > 0) {
    container.removeChild(container.lastElementChild);
  }

  if (number > 1) {
    number--;
  }
});