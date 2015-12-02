(function() {
    $('form').submit(function(e) {
        e.preventDefault();

        var postJson = $(this).serializeArray()
            .reduce(function(accum, item) {
                accum[item.name] = item.value;
                return accum;
            }, {});
        console.log(postJson);

        $.post('/lake-gif', postJson, function(data) {
            console.log(data);
            $('#lake-animation').attr('src', data + '?' + Math.random());
        }, 'json');
    });
})();
