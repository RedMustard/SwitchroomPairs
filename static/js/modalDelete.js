var entryData = {};

$("#modal-delete-button").on('click', function(event) {
	$('#delete-modal').modal('hide');

	$.ajax({
		url: "/delete",
		type: "POST",
		data: entryData,
		success: function(response) {
			setTimeout('goToIndex()', 500);
		}
	});
});


function deleteEntry() {
	$('#delete-modal').modal('show');
	getEntryInfo();
}


function getEntryInfo() {
	var entryFields = ["circuit-id-info", "cl-pair-info", "uo-pair-info"];

	entryData = {
		"circuit_id" : document.getElementById(entryFields[0]).innerText,
		"cl_pair" : document.getElementById(entryFields[1]).innerText,
		"uo_pair" : document.getElementById(entryFields[2]).innerText
	};
}


function goToIndex() {
	window.location = 'index';
}