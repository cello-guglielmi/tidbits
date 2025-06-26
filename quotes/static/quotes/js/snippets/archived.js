// === Quote Card Caching ===
window.quoteCache = new Map();
document.body.addEventListener("htmx:afterSwap", function(evt) {
    /*
    htmx docu:
    detail.target - the target of the request
    detail.xhr - the XMLHttpRequest
    detail.elt - the swapped in element
    */
    const item = evt.detail.elt.closest('.quote-item');
    if (!item) return;
    const id = item.dataset.id;
    const card = evt.detail.xhr.responseText;
    if (id) {
        quoteCache.set(id, card);
    }
    lucide.createIcons();
});

// === Initialize quote-list functions ===
export function initQuoteList() {
    const list = document.querySelector('.quote-list');
    const items = Array.from(list.children);
    const showMoreBtn = document.querySelector('.show-more-button');
    const searchInput = document.querySelector('.search-bar')

    if (searchInput) {
        searchInput.addEventListener('keyup', keywordFilter);
    }

    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', () => {
            updateList();
        });
    }
}

// === Quote Card Toggling ===
document.body.addEventListener('click', function(evt) {
    const item = evt.target.closest('.quote-item')
    if (!item) return;
    const card = evt.target.closest('.quote-card');
    const preview = evt.target.closest('.quote-preview');
    if (preview) {
        expandQuote(preview, item);
        return;
    }
    if (card) {
        collapseQuote(card, item);
    }
});

function expandQuote(preview, item) {
    const id = item.dataset.id;
    console.log(preview, item, id);
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

// === List Filtering Management ===
let visibleCount = BATCH_SIZE;
let shownItems = items.slice();

function updateList() {
    items.forEach((item, idx) => {
        const inFilter = shownItems.includes(item);
        const inOrder = shownItems.indexOf(item) < visibleCount;
        item.style.display = (inFilter && inOrder) ? 'list-item' : 'none';
    });
    // if (shownItems.length > visibleCount){
    //     showMoreBtn.style.display = 'block';
    // } else {
    //     showMoreBtn.style.display = 'none';
    // }
    showMoreBtn.style.display = (shownItems.length > visibleCount) ? 'block' : 'none';
    
}

function keywordFilter() {
    const txt = searchInput.value.trim().toUpperCase()
    shownItems = items.filter(item => item.dataset.fulltxt.toUpperCase().includes(txt));
    // visibleCount = BATCH_SIZE;
    updateList();

    // ul = document.querySelector('.quote-list');
    // li = ul.getElementsByTagName('li');
    // for (i = 0; i < li.length; i++) {
    //     txtValue = li[i].innerText;
    //     if (txtValue.toUpperCase().indexOf(filter) > -1) {
    //         li[i].style.display = "list-item";
    //     } else {
    //         li[i].style.display = "none";
    //     }
    // }
}
/*
Funnily enough,:

    ul = document.querySelector('.quote-list')
    li = ul.getElementsByTagName('li');

is roughly equivalent to below:

    li = document.querySelectorAll('.quote-list li');
*/
// initial render
updateList();

// === Old List Control ===

    switch (hxbtn.dataset.action) {
        case 'sort':
            const currSort = sort_val_Node.value;
            const sortBy = hxbtn.dataset.sortby
            const sameBtn = currSort === sortBy || currSort === '-' + sortBy;
            // Toggle direction if re-clicking the same button.
            const isAsc = sameBtn ? hxbtn.dataset.dir === 'desc' : hxbtn.dataset.dir === 'asc';
            
            const newSort = isAsc ? hxbtn.dataset.sortby : '-' + hxbtn.dataset.sortby;
            const newDir = isAsc ? 'asc' : 'desc';
            const ascIco = isAsc ? 'inline' : 'none';
            const descIco = isAsc ? 'none' : 'inline';

            hxbtn.querySelector('.sort-asc').style.display = ascIco;
            hxbtn.querySelector('.sort-desc').style.display = descIco;
            hxbtn.dataset.dir = newDir
            sort_val_Node.value = newSort;
            break;
        case 'loadmore':
            const currentCount = parseInt(page_count_Node.value) || 0;
            page_count_Node.value = currentCount + batch_size;
            break;
    }