(function() {
    function updateSlider(slider, label) {
        $('#' + slider).on('input change', function() {
            $('#' + label).html(this.value);
        });
    }

    var sliders = [
        {slider: 'animation-slider', label: 'animation-duration'},
        {slider: 'duration-slider', label: 'animation-duration'},
        {slider: 'tween-frames', label: 'frames-to-tween'},
        {slider: 'empty-frames', label: 'frames-at-end'},
    ];

    sliders.forEach(function(item) {
        updateSlider(item.slider, item.label);
    });

    $('#lake-animation-form').submit(function(e) {
        event.preventDefault();
        var lakeAnimation = $('#lake-animation');
        lakeAnimation.css('opacity', '0.3');


        var postJson = $(this).serializeArray()
            .reduce(function(accum, item) {
                accum[item.name] = item.value;
                return accum;
            }, {});

        $.post('/lake-gif', postJson)
            .done(function() {
                lakeAnimation.attr('src', '/lake-animation?' + Math.random())
                    .css('opacity', '1');
            });
    });

    $(function() {
        $('#generate-regular-gif').click(function() {
            event.preventDefault();
            var regularGif = $('#regular-gif');
            regularGif.css('opacity', '0.3');

            var form_data = new FormData($('#regular-gif-form')[0]);

            $.ajax({
                type: 'POST',
                url: '/upload-gif',
                data: form_data,
                contentType: false,
                processData: false
            }).done(function(data) {
                regularGif.attr('src', '/regular-gif?' + Math.random())
                    .css('opacity', '1');
            }).fail(function(data) {
                console.log(data);
                alert('error!');
            });
        });
    });
})();
