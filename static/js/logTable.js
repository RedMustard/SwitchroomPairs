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
	refresh: 'fa-refresh',
	toggle: 'fa-columns'
};


// Highlight table row on click
$table.on('click', 'tbody tr', function(event) {
	var $row = $(this).closest("tr");
	$(this).addClass('table-info').siblings().removeClass('table-info');
});


function getHeight() {
	var windowWidth = $(window).width();
	var windowHeight = $(window).height();
	var navHeight = $('#nav-bar').outerHeight(true);
	var formHeight = $('#field-container').outerHeight(true);
	var toolbarHeight = $('#toolbar').outerHeight(true);
	var bottomMargin = 55;

	if (windowWidth < 768) {
		return 500;
	} else if (windowWidth >= 768) {
		return windowHeight - navHeight - formHeight - toolbarHeight - bottomMargin;
	}
}