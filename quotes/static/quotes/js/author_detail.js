// === Swap & Cache Quote cards ===
const quoteCache = new Map();
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

// === List Management ===
const list = document.querySelector('.quote-list');
// const items = Array.from(list.querySelectorAll('li'));
const items = Array.from(list.children);
const showMoreBtn = document.querySelector('.show-more-button');
const searchInput = document.querySelector('.search-bar')

const BATCH_SIZE = 2;
let visibleCount = 2;
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

    // filter = input.value.toUpperCase();
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
Funnily enough, the above section:

    ul = document.querySelector('.quote-list')
    li = ul.getElementsByTagName('li');

is roughly equivalent to below:

    li = document.querySelectorAll('.quote-list li');
*/

showMoreBtn.addEventListener('click', () => {
    visibleCount += BATCH_SIZE;
    updateList();

    // const hiddenItems = Array.from(list.querySelectorAll('li'))
    //     .filter(li => getComputedStyle(li).display === 'none');
    // hiddenItems.slice(0, 2).forEach(li => li.style.display = 'list-item');
    // if (hiddenItems.length <= 2) {
    //     showMoreBtn.style.display = 'none';
    // }
});

searchInput.addEventListener('keyup', keywordFilter);

// initial render
updateList();
