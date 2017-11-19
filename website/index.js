$(document).ready(function(){
	$('#submit').click(function(event){
		var url = "";
		$('#result').css('display', 'block');
		$.getJSON(url, function(data) {
			$('#result').src(data.src);
		}).fail(function(jqXHR, textStatus, errorThrown) { $("#error").show(); });
	});
});