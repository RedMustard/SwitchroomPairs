var entryData = {};

$("#modal-delete-button").on('click', function(event) {
	$('#delete-modal').modal('hide');

	$.ajax({
		url: "delete",
		type: "POST",
		data: entryData,
		success: function(response) {
			setTimeout('reloadPage()', 250);
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


function reloadPage() {
	console.log(location.pathname);
	if  (location.href.indexOf('admin') > -1) {
		window.location = 'admin';
	} else if ((location.href.indexOf('index') > -1) || (location.href.indexOf('/') > -1)) {
		window.location = 'index';
	}
}