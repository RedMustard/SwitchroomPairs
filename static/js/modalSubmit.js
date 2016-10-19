var formData = {};


$("#modal-submit-button").on('click', function(event) {
	$('#submit-modal').modal('hide');

	$.ajax({
		url: "submit",
		type: "POST",
		data: formData,
		success: function(response) {
			setTimeout('reloadPage()', 500);
		}
	});
});


function submitForm() {
	var valid = validateInput();

	if(valid) {
		$('#submit-modal').modal('show');
		getSubmitFormInput();
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


function getSubmitFormInput() {
	var formFields = ['circuit-id', 'circuit-type', 'cl-pair', 'uo-pair', 'customer-name', 
		'customer-phone', 'notes-field'];

	var modalFields = ['submit-circuit', 'submit-type', 'submit-cl-pair', 'submit-uo-pair',
		'submit-name', 'submit-phone', 'submit-notes'];

	for (var i = 0; i < modalFields.length; i++) {
		currentFormField = document.getElementById(formFields[i]).value;
		document.getElementById(modalFields[i]).innerHTML = "" + currentFormField;
	}

	formData = {
		"circuit_id" : document.getElementById(formFields[0]).value,
		"circuit_type" :document.getElementById(formFields[1]).value,
		"cl_pair" : document.getElementById(formFields[2]).value,
		"uo_pair" : document.getElementById(formFields[3]).value,
		"customer_name" : document.getElementById(formFields[4]).value,
		"customer_phone" : document.getElementById(formFields[5]).value,
		"notes" : document.getElementById(formFields[6]).value
	};
}


function reloadPage() {
	console.log(location.pathname);
	if ((location.href.indexOf('index') > -1) || (location.href.indexOf('/') > -1)) {
		window.location = 'index';
	} else if (location.href.indexOf('/admin') > -1) {
		window.location = 'admin';
	}
}