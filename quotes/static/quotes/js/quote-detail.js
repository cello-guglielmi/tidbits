import { showModal } from './share-modal.js';


export function initQuoteCards(scope = document) {
    document.body.addEventListener('click', function(evt) {
        const item = evt.target.closest('.object-item')
        if (!item) return;
        const card = evt.target.closest('.object-card');
        //const preview = evt.target.closest('.quote-preview');
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
        // if (preview) {
        //     expandQuote(preview, item);
        //     return;
        // }
        // if (card) {
        //     collapseQuote(card, item);
        // }
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