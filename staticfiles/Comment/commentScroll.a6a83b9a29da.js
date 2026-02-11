function scrollToComment(commentId) {
    // element which needs to be scrolled to
    var comment = document.getElementById('comment-' + commentId);

    if (comment) {
        // scroll to element
        comment.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Add a highlight effect
        comment.style.backgroundColor = '#fff3cd';
        setTimeout(() => {
            comment.style.backgroundColor = '';
        }, 3000);
    }
}