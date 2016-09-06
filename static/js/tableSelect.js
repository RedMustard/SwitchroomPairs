$('#databaseTable').on('click', 'tbody tr', function(event) {
	$(this).addClass('table-info').siblings().removeClass('table-info');
	console.log( $(this).text() );
});

// $(document).on('click', 'tr', function() {
// 	$(this).addClass('table-info');
// });

// $('#databaseView').click(function() {
   // $(this).addClass('table-info');
// });





// window.onload = function() {
// 	var databaseTable = document.getElementById('databaseTable');
// }

// databaseTable.onclick = function() {
// 	// $(this).addClass('table-info');
// 	console.log( "sadsadsadsasad" );
// }