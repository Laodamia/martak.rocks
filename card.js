// Flip card that shows a random item from window.CARD_ITEMS
(function () {
  const items = window.CARD_ITEMS;
  const card = document.getElementById("qcard");
  const text = document.getElementById("q");
  let last = -1;
  function draw() {
    let i;
    do { i = Math.floor(Math.random() * items.length); } while (i === last && items.length > 1);
    last = i;
    text.textContent = items[i];
  }
  card.addEventListener("click", () => {
    if (!card.classList.contains("flipped")) draw();
    card.classList.toggle("flipped");
  });
  document.getElementById("again").addEventListener("click", () => {
    if (card.classList.contains("flipped")) {
      card.classList.remove("flipped");
      setTimeout(() => { draw(); card.classList.add("flipped"); }, 450);
    } else { draw(); card.classList.add("flipped"); }
  });
})();
