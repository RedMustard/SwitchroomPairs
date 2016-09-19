var formData = {};


$("#modal-edit-button").on('click', function(event) {
	var valid = validateInput();

	if (valid) {
		getFormInput();

		$('#edit-modal').modal('hide');

		$.ajax({
			url: "/edit",
			type: "POST",
			data: formData,
			success: function(response) {
				setTimeout('goToIndex()', 500);
			}
		});
	}
});


function setFormInputs() {
	var formFields = ["circuit-id-info", "circuit-type-info","cl-pair-info",
		"uo-pair-info", "customer-name-info", "customer-phone-info", "notes-info"];

	var modalFields = ['edit-circuit-id', 'edit-circuit-type', 'edit-cl-pair', 
		'edit-uo-pair', 'edit-customer-name', 'edit-customer-phone', 
		'edit-notes-field'];

	for (var i = 0; i < modalFields.length; i++) {
		currentFormField = document.getElementById(formFields[i]).innerText;
		document.getElementById(modalFields[i]).value = currentFormField;
	}
}


function getFormInput() {
	var formFields = ['edit-circuit-id', 'edit-circuit-type', 'edit-cl-pair', 
		'edit-uo-pair', 'edit-customer-name', 'edit-customer-phone', 
		'edit-notes-field'];

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


function editEntry() {
	$('#edit-modal').modal('show');
	setFormInputs();
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




function goToIndex() {
	window.location = 'index';
}