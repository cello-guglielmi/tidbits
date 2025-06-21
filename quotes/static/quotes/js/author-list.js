
const sort_val_Node = document.querySelector('input[name="sort_value"]');
const page_count_Node = document.querySelector('input[name="page_count"]');
const batch_size = 5;
page_count_Node.value = batch_size;

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
            page_count_Node.value = currentCount + batch_size;
            break;
    }
});
