export function initQuoteList() {
    const list = document.querySelector('.quote-list');
    const items = Array.from(list.children);
    const showMoreBtn = document.querySelector('.show-more-button');
    const searchInput = document.querySelector('.search-bar')

    const tagbox = document.querySelector('.tag-box');
    const legend = tagbox.querySelector('.mood-title');
    const content = tagbox.querySelector('div');
    //
    run_quotelist();

    document.body.addEventListener('htmx:afterSwap', function(evt) {
        if (evt.target.id !== 'quote-list') return;
        run_quotelist();
    });


}

let tagExpanded = false;
export function run_quotelist() {
    const tagbox = document.querySelector('.tag-box');
    const legend = tagbox.querySelector('.mood-title');
    const content = tagbox.querySelector('div');

    legend.style.cursor = 'pointer'; // Make the legend clickable

    // content.style.display = 'none'; // Initially hide the content
    legend.addEventListener('click', function() {
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
    });
}