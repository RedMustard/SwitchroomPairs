var editData = {};


function setEditFormInputs() {
	var formFields = ["circuit-type-info","cl-pair-info",
		"uo-pair-info", "notes-info"];

	var modalFields = ['edit-circuit-type', 'edit-cl-pair', 
		'edit-uo-pair', 'edit-notes-field'];

	for (var i = 0; i < modalFields.length; i++) {
		currentFormField = document.getElementById(formFields[i]).innerText;
		document.getElementById(modalFields[i]).value = currentFormField;
	}
}


function editEntry() {
	$('#edit-modal').modal('show');
	setEditFormInputs();
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


$('#editCircuitForm').submit(function() {
	$('#edit-cl-pair').removeAttr('disabled');
	$('#edit-uo-pair').removeAttr('disabled');
});