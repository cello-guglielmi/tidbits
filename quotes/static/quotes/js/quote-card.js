import { showModal } from './share-modal.js';
import { initShareModal } from './share-modal.js';


export function initQuoteCards(scope = document) {
    document.body.addEventListener('click', function(evt) {
        const card = evt.target.closest('.object-card');
        if (!card) return;
        //const preview = evt.target.closest('.quote-preview');
        const btn = evt.target.closest('.footer-btn');
        if (btn) {
            evt.stopPropagation();
            const txt = card.querySelector('.quote-sentence').textContent;
            const author = card.querySelector('.quote-author').textContent;
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
    });
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

initShareModal();
initQuoteCards();