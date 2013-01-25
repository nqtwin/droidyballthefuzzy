function mouseBlah(className,color) {
$(className).mouseover(function() { $(this).css("color",color) });
}

function isDone(isItDone) {
	if (isItDone == "True") {
		$("#is-not-done").css("display","none");
		$("#select-date-done").css("display","none");
		$("#is-done").css("display","inline-block");
	}
}

$(document).ready(function() {
	//isDone(true);
//$(".entry-title").mouseleave(function() { $(this).css("color","blue") });
//$("#checkbox").css("visibility","visible");
//$(".entry-title").css("color","blue");
});