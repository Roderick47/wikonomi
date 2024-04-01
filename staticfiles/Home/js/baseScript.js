
    /* Functions for autocomplete.*/
    $(function(){
        $("#search").autocomplete({
            source:"{% url 'Search:autocomplete' %}",
            minLength: 2,
        });
    });

/* Initialize all tool tips */
// $(function(){
//     $('[data-toggle="tooltip"]').tooltip()
// });


// Set the width of the side navigation to 250px
// function openNav(){
//     document.getElementById('mySidenav').style.width = '250px';
//     document.getElementById('main').style.marginLeft = '250px';
//     document.body.style.backgroundColor = "rgba(0,0,0,0,0.4)";
    
// }

// Set the width of the side navigation to 0px.
// function closeNav(){
//     document.getElementById('mySidenav').style.width = '0';
//     document.getElementById('main').style.marginLeft = '0';
//     document.body.style.backgroundColor = "white";
// }


// function toggleSidebar(){
//     var sidebar = document.getElementById('mySidenav');
//     if (sidebar.style.width=="250px"){
//         closeNav();
//     } else{
//         openNav();
//     }
// }


// var btnSideBar = document.getElementById("sbButton");
// console.log(btnSideBar);
// btnSideBar.addEventListener("click", openNav);
// btnSideBar.addEventListener("click", closeNav);

