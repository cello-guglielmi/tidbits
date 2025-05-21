import { initShareModal } from './share-modal.js';
import { initQuoteCards } from './quote-detail.js';
import { initQuoteList } from './quote_list.js';

function initComponents(scope = document) {
    initShareModal(scope);
    initQuoteCards(scope);
    initQuoteList(scope);
}

document.body.addEventListener("htmx:afterSettle", function(evt) {
    if (evt.detail.target.id === "list-container") {
        initComponents();
        lucide.createIcons();
    }
});