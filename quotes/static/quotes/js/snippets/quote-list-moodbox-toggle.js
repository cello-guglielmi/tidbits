/* Toggle div inside tagbox on click! */
const tagbox = document.getElementById('tag-box');
const moodTitleBtn = document.getElementById('mood-title');
const moodContent = document.getElementById('mood-filter');
let tagExpanded = false;
document.addEventListener('click', function(evt) {
    if (evt.target == title) {
        if (tagExpanded) {
            moodContent.style.maxHeight = '0';
            tagbox.style.marginBottom = '0';
            setTimeout(() => {
                tagbox.style.borderColor = 'transparent';
                tagbox.style.background = 'transparent';
            }, 400);
        } else {
            moodContent.style.maxHeight = moodContent.scrollHeight + 'px';
            tagbox.style.borderColor = '#333';
            tagbox.style.background = 'white';
            tagbox.style.marginBottom = '10px';
        }
        tagExpanded = !tagExpanded;
    }
});