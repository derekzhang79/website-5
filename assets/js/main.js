$(document).ready(function() {

    $.each($('[data-behavior="links"]').find('a i'), function(i, sprite) {
        var $sprite = $(sprite);
        $sprite.data('class', $sprite.attr('class'));

        $sprite
            .on('mouseenter', function(){
                $sprite.removeClass();
                $sprite.addClass($sprite.data('class') + '-active');
            })

            .on('mouseleave', function(){
                $sprite.removeClass();
                $sprite.addClass($sprite.data('class'));
            });
    });

});