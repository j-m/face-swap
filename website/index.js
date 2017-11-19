$(document).ready(function(){
	var busy = false;
	$('form').submit(function( event ) {
		event.preventDefault();
		if(busy==false){
			busy = true;
			var url = "http://4076c2c2.ngrok.io/get-child?father="+$('#father').val()+"&mother="+$('#mother').val();
			$('#result').css('max-width','20rem');
			$('#result').css('max-height','20rem');
			$.getJSON(url, function(data) {
				$('#result').src(data.image_url);
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