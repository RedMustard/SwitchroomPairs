var rowData = [];
var $table = $('#database-table');

// Initialize table
$(function () {
	$table.bootstrapTable('resetView', { height: getHeight() } );
});


$(window).resize(function () {
	$table.bootstrapTable('resetView', {
		height: getHeight()
	});
});


window.icons = {
	print: 'fa-print',
	export: 'fa-external-link',
	columns: 'fa-th-list',
	refresh: 'fa-refresh'
};


window.onload = function() {
	selectFirstTableRow();
}


// Highlight table row on click
$table.on('click', 'tbody tr', function(event) {
	var $row = $(this).closest("tr");
	$(this).addClass('table-info').siblings().removeClass('table-info');
	populateInfoList($row);
});


function selectFirstTableRow() {
	var $body = $table.find("tbody"),
		$row = $body.find("tr:first");
	$row.addClass('table-info').siblings().removeClass('table-info');
	populateInfoList($row);
}


function getHeight() {
	var windowWidth = $(window).width();
	var windowHeight = $(window).height();
	var navHeight = $('#nav-bar').outerHeight(true);
	var formHeight = $('#field-container').outerHeight(true);
	var toolbarHeight = $('#toolbar').outerHeight(true);
	var bottomMargin = 70;

	if (windowWidth < 768) {
		return 500;
	} else if (windowWidth >= 768) {
		return windowHeight - navHeight - formHeight - toolbarHeight - bottomMargin;
	}
}


function populateInfoList(row) {
	var $tds = row.find("td");

	var infoFieldArray = ['circuit-id-info', 'circuit-type-info', 'cl-pair-info', 'uo-pair-info', 
		'customer-name-info', 'customer-phone-info', 'notes-info', 'date-info'];

	$.each($tds, function() {
		rowData.push($(this).text());	
	});

	for (var i = 0; i < infoFieldArray.length; i++) {
		document.getElementById(infoFieldArray[i]).innerHTML = "" + rowData[i];
	}

	rowData = [];
}