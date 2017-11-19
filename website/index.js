$(document).ready(function(){
	var busy = false;
	$('form').submit(function( event ) {
		event.preventDefault();
		if(busy==false){
			busy = true;
			var url = "";
			$('#result').css('display', 'block');
			var send = {father:$('#father').val(), mother:$('#mother').val()};
			$.getJSON(url, send)
			.done(function(data) {
				$('#result').src(data.src);
				busy = false;
			})
			.fail(function(jqXHR, textStatus, errorThrown) { $("#error").show(); });
		}
	});
	$( "input" ).keyup(function() {
		this.setAttribute('value', this.value);
		this.setAttribute('data-hadFocus', true);
	});
});