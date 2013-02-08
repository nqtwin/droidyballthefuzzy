	var str = "Live your lives with the desire to discover what's out there.";

	var spans = '<span>' + str.split("").join('</span><span>') + '</span>';
	
	var strWithLink = "Live your lives with the desire to discover <a href= {{url}}> what's out there.  </a>";
	
	var DELAY_TIME = 60;
	
	var FADE_IN_TIME = 1000;
	
	
$(document).ready(function() {
	$(spans).hide().appendTo('#letter-content').each(function(i) {
    	$(this).delay(DELAY_TIME * i).fadeIn(FADE_IN_TIME);
	});
	
	var waitTime = 60 * str.split("").length + FADE_IN_TIME;
	
	setTimeout(
  		function() 
  		{
    		$('#letter-content').html(strWithLink);
  		}, waitTime);
	
});