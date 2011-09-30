(function($) {
    $(document).ready(function(){
        $('#top-batch-controlbar').hide();
        function previousPage(){
            var start = parseInt($('#cbr-start').text());
            var size = parseInt($('#cbr-size').text());
            var names_list = $('#cbr-controller .cbr-image');
            var base_url = $('#cbr-controller #cbr-extracturl').text();
            if (start - size >= 0){ 
                names_list.removeClass('active');
                for(i=0; i < size; i++){
                    var ctrl_tag = names_list.eq(start - size + i);
                    $('#cbr-imageslot-' + i).attr('src', base_url + ctrl_tag.text());
                    ctrl_tag.addClass('active');
                }
                $('#cbr-start').text(start - size);

                var old_val = parseInt($('#cbr-show-index').text());
                $('#cbr-show-index').text(old_val - 1);
            }
            return 0;
            //window.location.replace($('#top-batch-controlbar .next a').attr('href'));
        }

        function nextPage(){
            var start = parseInt($('#cbr-start').text());
            var size = parseInt($('#cbr-size').text());
            var names_list = $('#cbr-controller .cbr-image');
            var base_url = $('#cbr-controller #cbr-extracturl').text();
            if (start + size < names_list.length){ 
                names_list.removeClass('active');
                for(i=0; i < size; i++){
                    var ctrl_tag = names_list.eq(start + size + i);
                    $('#cbr-imageslot-' + i).attr('src', base_url + ctrl_tag.text());
                    ctrl_tag.addClass('active');
                }
                $('#cbr-start').text(start + size);
                var old_val = parseInt($('#cbr-show-index').text());
                $('#cbr-show-index').text(old_val + 1);
            }
            return 0;
            //window.location.replace($('#top-batch-controlbar .next a').attr('href'));
        }

        $(document).keydown(function(e) {
            switch(e.keyCode) { 
                case 37:
                    previousPage();
                    break;
    //            case 38: alert('up'); break;
                case 39:
                    nextPage();
                    break;
    //            case 40: alert('down'); break;

            }
        });
        $('#cbr-next-arrow').click(function(event){
            event.preventDefault();
            nextPage()        
        });
        $('#cbr-prev-arrow').click(function(event){
            event.preventDefault();
            previousPage()        
        });
        $('.cbr-arrow').css('display','inline-block');
        $('#cbr-switch-mode').click(function(event){
            event.preventDefault();
            $('.cbr-slotcontainer:first').insertAfter($('.cbr-slotcontainer').eq(1));
        });
    });
})(jQuery);

