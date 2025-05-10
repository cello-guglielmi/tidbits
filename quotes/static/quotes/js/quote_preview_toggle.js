const quoteCache = new Map();

document.body.addEventListener("htmx:afterSwap", function handler(evt) {
    const card = evt.detail.xhr.responseText;
    const id = evt.detail.target.dataset.id
    if (id) {
        quoteCache.set(id, card);
    }
});

function expandQuote(preview) {
    const id = preview.dataset.id;
    if (quoteCache.has(id)) {
        preview.outerHTML = quoteCache.get(id);
        return
    }
}

function collapseQuote(card) {
    card.outerHTML = `
        <div class="quote-preview"
            data-id="${card.dataset.id}"
            onclick="expandQuote(this)">
            ${card.dataset.previewtext}
        </div>`;
}