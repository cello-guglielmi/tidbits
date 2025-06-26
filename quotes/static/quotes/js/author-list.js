// HTMX collects inputs before click listeners run
// Using pointerdown to beat HTMX value collection
document.body.addEventListener('pointerdown', evt => {
    if (evt.button !== 0) return;
    const hxbtn = evt.target.closest('[data-action]');
    if (!hxbtn) return;
    const sort_tracker = document.getElementById('sort-tracker');
    const buttonSet = document.querySelectorAll('.sort-button')
    buttonSet.forEach(btn => {
        btn.classList.remove('sort-button-active');
        btn.classList.add('sort-button-deactive');
    });
    hxbtn.classList.remove('sort-button-deactive');
    hxbtn.classList.add('sort-button-active');

    const currSort = sort_tracker.value;
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
    sort_tracker.value = newSort;
});
