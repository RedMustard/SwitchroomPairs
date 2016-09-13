$('#database-table').on('click', 'tbody tr', function(event) {
	$(this).addClass('table-info').siblings().removeClass('table-info');
	console.log( $(this).text().replace(/ /g,''));
});
