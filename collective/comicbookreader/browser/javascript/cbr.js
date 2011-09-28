(function($) {
    $(document).keydown(function(e) {
        switch(e.keyCode) { 
            case 37:
                if ($('#top-batch-controlbar .previous a').length > 0){
                    window.location.replace($('#top-batch-controlbar .previous a').attr('href'));
                }
                break;
//            case 38: alert('up'); break;
            case 39:
                if ($('#top-batch-controlbar .next a').length > 0){
                    window.location.replace($('#top-batch-controlbar .next a').attr('href'));
                }
                break;
//            case 40: alert('down'); break;

        }
    });
})(jQuery);

