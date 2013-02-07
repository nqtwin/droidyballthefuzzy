var str = $('Hello World').text();

var spans = '<span>' + str.split(/\s+/).join(' </span><span>') + '</span>';

$(spans).hide().appendTo('#letter-content').each(function(i) {
    $(this).delay(400 * i).fadeIn();
});