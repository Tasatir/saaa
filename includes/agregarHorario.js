$(document).ready(function(){

	$('#time1').timepicker({
		hourMin: 6,
		hourMax: 21
	});
	$('#time2').timepicker({
		hourMin: 6,
		hourMax: 21
	});
	$('#time1').keydown(function() {return false;});
	$('#time2').keydown(function() {return false;});

});
