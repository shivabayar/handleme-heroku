(function (){
   "use strict";

    $("#search_button" ).click(function() {
        var searchText = $('#search_box').val();
        window.location.href = "search/twitter/timeline/" + searchText + "/";
    });
})();
