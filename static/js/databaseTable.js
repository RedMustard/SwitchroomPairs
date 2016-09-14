var rowData = [];

// Initialize table
$(function () {
	var $table = $('#database-table');
	$table.bootstrapTable('resetView', { height: getHeight() } );

	$(window).resize(function () {
		$table.bootstrapTable('resetView', {
			height: getHeight()
		});
	});
});


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


function populateInfoList() {
	var circuitID = document.getElementById('circuit-id-info'),
		circuitType = document.getElementById('circuit-type-info'),
		clPair = document.getElementById('cl-pair-info'),
		uoPair = document.getElementById('uo-pair-info'),
		customerName = document.getElementById('customer-name-info'),
		customerPhone = document.getElementById('customer-phone-info'),
		notes = document.getElementById('notes-info'),
		date = document.getElementById('date-info');

	circuitID.innerHTML = "" + rowData[0];
	circuitType.innerHTML = "" + rowData[1];
	clPair.innerHTML = "" + rowData[2];
	uoPair.innerHTML = "" + rowData[3];
	customerName.innerHTML = "" + rowData[4];
	customerPhone.innerHTML = "" + rowData[5];
	notes.innerHTML = "" + rowData[6];
	date.innerHTML = "" + rowData[7];

	rowData = [];

	// for(var i=0; i < rowData.length; i++) {
	// 	console.log(rowData[i].toString());
	// }


	// document.getElementById('circuit-id-info').innerHTML = 'fdsfasfd';
	// $.each(rowData, function() {
	// 	console.log($(this).text());
	// });

	// console.log(circuitID);
}