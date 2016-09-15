formData = [];
var $form = $('#circuitForm'),
	$submit = $('#submitButton'); // Add id to submit button


$form.on('click', 'tbody tr', function(event) {
	$(this).addClass('table-info').siblings().removeClass('table-info');

	var $row = $(this).closest("tr"),
		$tds = $row.find("td");

	$.each($tds, function() {
		rowData.push($(this).text());	
	});

	populateInfoList();
});