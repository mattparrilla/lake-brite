(function() {
    $('form').submit(function(e) {
        e.preventDefault();
        var lakeAnimation = $('#lake-animation');
        lakeAnimation.css('opacity', '0.3');


        var postJson = $(this).serializeArray()
            .reduce(function(accum, item) {
                accum[item.name] = item.value;
                return accum;
            }, {});

        $.post('/lake-gif', postJson)
            .done(function(data) {
                console.log('success');
                console.log(data);
                lakeAnimation.attr('src', '/image?' + Math.random())
                    .css('opacity', '1');
            });
    });
})();
