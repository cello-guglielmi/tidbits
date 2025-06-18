export function initQuoteList() {
    const tagbox = document.getElementById('tag-box');
    const moodTitleBtn = document.getElementById('mood-title');
    const moodContent = document.getElementById('mood-filter');
    moodTitleBtn.style.cursor = 'pointer';
    // Make the legend clickable

    const sort_val_Node = document.querySelector('input[name="sort_value"]');
    const sort_dir_Node = document.querySelector('input[name="sort_dir"]');
    const page_count_Node = document.querySelector('input[name="page_count"]');
    // console.log('PC VALUE::::', page_count_Node.value)
    const batchSize = parseInt(document.getElementById('list-container').dataset.batchsize);
    // console.log('BATCH SIZE::::', batchSize)
    page_count_Node.value = batchSize;
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
                const sortAscIco = hxbtn.querySelector('.sort-asc');
                const sortDescIco = hxbtn.querySelector('.sort-desc');
                const sortBy = hxbtn.dataset.sortby
                const isAsc = hxbtn.dataset.dir === 'asc';
                // Toggle logic
                let newValue = isAsc ? sortBy : '-' + sortBy;
                const sameButtonClick = newValue === sort_val_Node.value;
                let newDir = hxbtn.dataset.dir; // Start as oldDir
                // Only change dir if same button click
                if (sameButtonClick) {
                    newValue = isAsc ? '-' + sortBy : sortBy;
                    newDir = isAsc ? 'desc' : 'asc';
                    sortAscIco.style.display = isAsc ? 'none' : 'inline';
                    sortDescIco.style.display = isAsc ? 'inline' : 'none';
                }
                sort_dir_Node.value = newDir;
                hxbtn.dataset.dir = newDir;
                sort_val_Node.value = newValue;
                break;
            case 'loadmore':
                const currentCount = parseInt(page_count_Node.value) || 0;
                // console.log('currentCount:', currentCount, 'batchSize:', batchSize);
                // console.log(currentCount, '+', batchSize, '=', currentCount + batchSize);
                page_count_Node.value = currentCount + batchSize;
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