var formData = {};

function submitForm() {
	var valid = validateInput();

	if(valid) {
		$('#submit-modal').modal('show');

		getFormInput();
	}
}


function validateInput() {
	var formFields = ['circuit-id', 'circuit-type', 'cl-pair', 'uo-pair'];

	for (var i = 0; i < formFields.length; i++) {
		var currentField = document.getElementById(formFields[i]);

		if (currentField.value == null || currentField.value == "") {
			return false;
		}
	}

	return true;
}

// 'circuit_id', 'circuit_type', 'cl_pair', 'uo_pair', 'customer_name', 'customer_phone', 'notes'

function getFormInput() {
	var formFields = ['circuit-id', 'circuit-type', 'cl-pair', 'uo-pair', 'customer-name', 
		'customer-phone', 'notes-field'];

	var modalFields = ['submit-circuit', 'submit-type', 'submit-cl-pair', 'submit-uo-pair',
		'submit-name', 'submit-phone', 'submit-notes'];

	for (var i = 0; i < modalFields.length; i++) {
			currentFormField = document.getElementById(formFields[i]).value;
			// formData.push(currentFormField);

			document.getElementById(modalFields[i]).innerHTML = "" + currentFormField;
	}



	formData = {
		"circuit_id" : document.getElementById(formFields[0]).value ,
		"circuit_type" :document.getElementById(formFields[1]).value ,
		"cl_pair" : document.getElementById(formFields[2]).value,
		"uo_pair" : document.getElementById(formFields[3]).value,
		"customer_name" : document.getElementById(formFields[4]).value,
		"customer_phone" : document.getElementById(formFields[5]).value,
		"notes" : document.getElementById(formFields[6]).value
	};
}


$("#modal-submit-button").on('click', function(event) {
	$('#submit-modal').modal('hide');

	$.ajax({
		url: "/submit",
		type: "POST",
		data: formData,
		success: function(data, textStaus, jqXHR) {
			document.write(data);
		}
	});

	console.log(formData);

	
	// window.location.reload(true);
	// for (var i = 0; i < formData.length; i++) {
	// 	console.log(formData[i]);
	// }
});


// formData = [];
// var $form = $('#circuitForm'),
// 	$submit = $('#submitButton'); // Add id to submit button


// $form.on('click', 'tbody tr', function(event) {
// 	$(this).addClass('table-info').siblings().removeClass('table-info');

// 	var $row = $(this).closest("tr"),
// 		$tds = $row.find("td");

// 	$.each($tds, function() {
// 		rowData.push($(this).text());	
// 	});

// 	populateInfoList();
// });