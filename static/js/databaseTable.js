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
	columns: 'fa-th-list'
};


// Highlight table row on click
$('#database-table').on('click', 'tbody tr', function(event) {
	$(this).addClass('table-info').siblings().removeClass('table-info');

	var $row = $(this).closest("tr"),
		$tds = $row.find("td");

	$.each($tds, function() {
		rowData.push($(this).text());	
	});

	populateInfoList();
});


$('#database-table').on('load', 'tbody tr', function(event) {

})


function getHeight() {
	var windowWidth = $(window).width();
	var windowHeight = $(window).height();
	var navHeight = $('#nav-bar').outerHeight(true);
	var formHeight = $('#field-container').outerHeight(true);
	var toolbarHeight = $('#toolbar').outerHeight(true);
	var bottomMargin = 100;

	if (windowWidth < 768) {
		return 500;
	} else if (windowWidth >= 768) {
		return windowHeight - navHeight - formHeight - toolbarHeight - bottomMargin;
	}
}


function populateInfoList() {
	infoFieldArray = ['circuit-id-info', 'circuit-type-info', 'cl-pair-info', 'uo-pair-info', 
		'customer-name-info', 'customer-phone-info', 'notes-info', 'date-info'];

		for (var i = 0; i < infoFieldArray.length; i++) {
			document.getElementById(infoFieldArray[i]).innerHTML = "" + rowData[i];
		}

	rowData = [];
}