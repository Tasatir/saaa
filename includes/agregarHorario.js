$(document).ready(function(){

	$('#time').timepicker({
		hourMin: 6,
		hourMax: 21
	});
	$('#time').keydown(function() {return false;});

});
