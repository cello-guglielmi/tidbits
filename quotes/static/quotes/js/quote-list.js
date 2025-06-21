import { initShareModal } from './share-modal.js';
import { initQuoteCards } from './quote-detail.js';

function initQuoteList() {
    const tagbox = document.getElementById('tag-box');
    const moodTitleBtn = document.getElementById('mood-title');
    const moodContent = document.getElementById('mood-filter');
    moodTitleBtn.style.cursor = 'pointer';
    // Make the legend clickable

    const sort_val_Node = document.querySelector('input[name="sort_value"]');
    const page_count_Node = document.querySelector('input[name="page_count"]');
    const batch_size = parseInt(document.querySelector('input[name="batchsize"]').value);
    // console.log('BATCH SIZE::::', batch_size)
    page_count_Node.value = batch_size;
    // console.log('NOW PC VALUE::::', page_count_Node.value)

    // Using pointerdown to beat HTMX to value collection
    // HTMX collects inputs before click listeners run, so we need to mutate state earlier
    document.body.addEventListener('pointerdown', evt => {
        if (evt.button !== 0) return;
        const hxbtn = evt.target.closest('[data-action]');
        if (!hxbtn) return;
        const buttonSet = document.querySelectorAll('.sort-button')
        buttonSet.forEach(btn => {
            btn.classList.remove('sort-button-active');
            btn.classList.add('sort-button-deactive');
        });
        hxbtn.classList.remove('sort-button-deactive');
        hxbtn.classList.add('sort-button-active');
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
                // console.log('currentCount:', currentCount, 'batch_size:', batch_size);
                // console.log(currentCount, '+', batch_size, '=', currentCount + batch_size);
                page_count_Node.value = currentCount + batch_size;
                // console.log(page_count_Node.value)
                break;
        }
    });

    tagbox.addEventListener('mouseleave', () => {
        moodContent.style.maxHeight = '0';
        tagbox.style.padding = '2px 0.5em';
    });
    tagbox.addEventListener('mouseenter', () => {
        moodContent.style.maxHeight = moodContent.scrollHeight + 'px';
        tagbox.style.padding = '0.5em';
    });
}

function initComponents(scope = document) {
    initShareModal(scope);
    initQuoteCards(scope);
    initQuoteList(scope);
}

initComponents();
lucide.createIcons();