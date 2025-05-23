export function initQuoteList() {
    const tagbox = document.getElementById('tag-box');
    const title = document.getElementById('mood-title');
    const content = document.getElementById('mood-filter');
    let tagExpanded = false;
    title.style.cursor = 'pointer';
    // Make the legend clickable

    const sort_val_Node = document.querySelector('input[name="sort_value"]');
    const sort_dir_Node = document.querySelector('input[name="sort_dir"]');
    const dirLabel = document.getElementById('dir-label');
    const page_count_Node = document.querySelector('input[name="page_count"]');
    console.log('PC VALUE::::', page_count_Node.value)
    const batchSize = parseInt(document.getElementById('list-container').dataset.batchsize);
    console.log('BATCH SIZE::::', batchSize)
    page_count_Node.value = batchSize;
    console.log('NOW PC VALUE::::', page_count_Node.value)

    // Using pointerdown to beat HTMX to value collection
    // HTMX collects inputs before click listeners run, so we need to mutate state earlier
    document.body.addEventListener('pointerdown', evt => {
        if (evt.button !== 0) return;
        const hxbtn = evt.target.closest('[data-action]');
        if (!hxbtn) return;
        switch (hxbtn.dataset.action) {
             case 'sort':
                const isAsc = sort_dir_Node.value === 'asc';
                const sortval = hxbtn.dataset.sortval
               //
                sort_val_Node.value = isAsc ? sortval : '-' + sortval;
                const newDir = isAsc ? 'desc' : 'asc';
                sort_dir_Node.value = newDir
                dirLabel.textContent = newDir;
                break;
            case 'loadmore':
                const currentCount = parseInt(page_count_Node.value) || 0;
                console.log('currentCount:', currentCount, 'batchSize:', batchSize);
                console.log(currentCount, '+', batchSize, '=', currentCount + batchSize);
                page_count_Node.value = currentCount + batchSize;
                console.log(page_count_Node.value)
                break;
        }
    });

    document.addEventListener('click', function(evt) {
        if (evt.target == title) {
            if (tagExpanded) {
                content.style.maxHeight = '0';
                tagbox.style.marginBottom = '0';
                setTimeout(() => {
                    tagbox.style.borderColor = 'transparent';
                    tagbox.style.background = 'transparent';
                }, 500);
            } else {
                content.style.maxHeight = content.scrollHeight + 'px';
                tagbox.style.borderColor = '#333';
                tagbox.style.background = 'white';
                tagbox.style.marginBottom = '10px';
            }
            tagExpanded = !tagExpanded;
        }
    });
}