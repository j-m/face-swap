$(document).ready(function(){
	var busy = false;
	$('form').submit(function( event ) {
		event.preventDefault();
		if(busy==false){
			busy = true;
			$("#result").attr('src',"http://thinkfuture.com/wp-content/uploads/2013/10/loading_spinner.gif");
			var url = "http://4076c2c2.ngrok.io/get-child?father="+encodeURIComponent($('#father').val())+"&mother="+encodeURIComponent($('#mother').val());
			$('#result').css('max-width','20rem');
			$('#result').css('max-height','20rem');
			$.ajax({
				'url': url,
				'success': function(json) { 
					$("#result").attr('src', json); 
					busy = false;
				},
				'error': function() {
					console.log('Failed');
					$("#error").show();
				}
			});
		}
	});
	$( "input" ).keyup(function() {
		this.setAttribute('value', this.value);
		this.setAttribute('data-hadFocus', true);
	});
});