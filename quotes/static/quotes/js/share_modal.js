const modal = document.querySelector('.share-modal');

function hideModal(){
    modal.classList.remove("show");
}

document.addEventListener('keydown', function(evt) {
if (evt.key === 'Escape' && modal.classList.contains('show')) {
        hideModal();
    }
});

document.addEventListener('click', function(evt) {
    if (!modal.contains(evt.target) && modal.classList.contains('show')){
        hideModal();
    }
});

modal.addEventListener('click', function(evt) {
    const close = evt.target.closest('.close');
    if (close && modal.classList.contains('show')){
        hideModal();
    }
});

function isMobile() {
  const regex = /Android|webOS|iPhone|iPad|iPod|BlackBerry|Windows Phone/i;
  return regex.test(navigator.userAgent);
}

export function showModal(text, author, card) {
  if (isMobile()) {
    navigator.share({
      text: `"${text}" — ${author}`
    }).catch(err => console.log('Share canceled or failed:', err));
    return
  }
    // Set modal text
    modal.querySelector('.modal-text').textContent = `"${text}"`;
    modal.querySelector('.modal-author').textContent = `— ${author}`;
  // 1. Measure
  const cardRect  = card.getBoundingClientRect();
  const modalRect = modal.getBoundingClientRect();
  // 2. Compute
  const top  = cardRect.top + window.scrollY   // top of card in page coords
             + (cardRect.height  - modalRect.height) / 2;  // center modal over card

  const left = cardRect.left + window.scrollX // left of card in page coords
             + (cardRect.width  - modalRect.width) / 2; // center modal over card
    // 3. Position
    modal.style.top = `${top}px`;
    modal.style.left = `${left}px`
    modal.classList.add("show");
    //const url = encodeURIComponent(window.location.href);
    //const text = encodeURIComponent(`"${quote}" — ${author}`);
}