import { showModal } from './share_modal.js';

document.body.addEventListener('click', function(evt) {
    const item = evt.target.closest('.quote-item')
    if (!item) return;
    const btn = evt.target.closest('.footer-btn');
    if (btn) {
        evt.stopPropagation();
        const txt = item.dataset.fulltxt;
        const author = item.dataset.author;
        const func = btn.dataset.func;
        switch(func) {
            case 'copy':
                navigator.clipboard.writeText(`"${txt}" — ${author}`)
                    .then(() => copyToast(card, 'Quote copied to clipboard!'))
                    .catch(() => copyToast(card, 'Failed to copy quote.'));
                break;
            case 'like':
                
                break;
            case 'fave':

                break;
            case 'share':
                showModal(txt, author, card)
                break;
        }
        return;
    }
    const preview = evt.target.closest('.quote-preview');
    if (preview) {
        expandQuote(preview, item);
        return;
    }
    const card = evt.target.closest('.quote-card');
    if (card) {
        collapseQuote(card, item);
    }
});

function expandQuote(preview, item) {
    const id = item.dataset.id;
    //console.log(preview, item, id);
    if (quoteCache.has(id)) {
        preview.outerHTML = quoteCache.get(id);
    }
    lucide.createIcons();
}

function collapseQuote(card, item) {
    card.outerHTML = `
        <div class="quote-preview">
            ${item.dataset.prevtxt}
        </div>`;
}




function copyToast(card, message) {
  const toast = card.querySelector('.toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 1000); // visible for 1 second
}