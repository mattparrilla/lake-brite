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
        $('#submit').click(function() {
            event.preventDefault();
            var form_data = new FormData($('#uploadform')[0]);
            $.ajax({
                type: 'POST',
                url: '/uploadajax',
                data: form_data,
                contentType: false,
                processData: false,
                dataType: 'json'
            }).done(function(data, textStatus, jqXHR){
                console.log(data);
                console.log(textStatus);
                console.log(jqXHR);
                console.log('Success!');
                $("#resultFilename").text(data['name']);
                $("#resultFilesize").text(data['size']);
            }).fail(function(data){
                alert('error!');
            });
        });
    }); 
})();
