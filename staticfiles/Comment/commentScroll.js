
function scrollToComment(){

    var data = JSON.parse({{data|escapejs}})

    // element which needs to be scrolled to
    var comment = document.getElementById(data[commentID]);
    
    // scroll to element
    comment.scrollIntoView({ behavior: 'smooth', block: 'end'});


}