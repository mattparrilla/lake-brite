(function() {
    $('#animation-slider').on('input change', function() {
        $('#animation-duration').html(this.value);
    });

    $('#lake-animation-form').submit(function(e) {
        e.preventDefault();
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
        $('#upload-file-btn').click(function() {
            var form_data = new FormData($('#upload-file')[0]);
            $.ajax({
                type: 'POST',
                url: '/uploadajax',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function(data) {
                    console.log('Success!');
                },
            });
        });
    });
})();
