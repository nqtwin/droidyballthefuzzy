function mouseBlah(className,color) {
$(className).mouseover(function() { $(this).css("color",color) });
}

$(document).ready(function() {
$(".entry-title").mouseleave(function() { $(this).css("color","blue") });
$("#checkbox").css("visibility","visible");
$(".entry-title").css("color","blue");
});