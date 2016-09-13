var $table = $('#database-table');
var $w = $(window)


$(function () {
	$table.bootstrapTable('resetView', { height: getHeight() } );

	$(window).resize(function () {
		$table.bootstrapTable('resetView', {
			height: getHeight()
		});
	});
});


function getHeight() {
	var bodyRect = document.body.getBoundingClientRect();
	var windowHeight = $(window).height();
	var windowWidth = $(window).width();
	var navHeight = $('#nav-bar').outerHeight(true);
	var formHeight = $('#field-container').outerHeight(true);
	var toolbarHeight = $('#toolbar').outerHeight(true);
	var bottomMargin = 140;


	var documentHeight = $(document).height();


	console.log(documentHeight);

	// console.log(bodyHeight);
	console.log(formHeight);
	console.log($(window).width())

	if (windowWidth < 768) {
		return 750;
	} else if (windowWidth >= 768) {

		return windowHeight - navHeight - formHeight - bottomMargin;
	}
	// return 250;
}


// Highlight table row on click
$('#database-table').on('click', 'tbody tr', function(event) {
	$(this).addClass('table-info').siblings().removeClass('table-info');
	console.log( $(this).text().replace(/ /g,''));
});





// function initTable() {
// 	$table.bootstrapTable({
// 		height: getHeight()
// 		// columns: [
// 		// 	[
// 		// 		{
// 		// 			title: 'Circuit ID',
// 		// 			field: 'id',
// 		// 			align: 'center',
// 		// 			sortable: 'true'

// 		// 		}
// 		// 	]
// 		// ]

// 	});

// 	setTimeout(function () {
// 		$table.bootstrapTable('resetView');
// 	}, 200);

// 	$(window).resize(function () {
// 		$table.bootstrapTable('resetView', {
// 			height: getHeight()
// 		});
// 	});
// }

// function getHeight() {
// 	return $(window).height() - $('h1').outerHeight(true);
// }

// $(function () {
// 	var scripts = [
// 			location.search.substring(1) || 'assets/bootstrap-table/src/bootstrap-table.js',
// 			'assets/bootstrap-table/src/extensions/export/bootstrap-table-export.js',
// 			'http://rawgit.com/hhurz/tableExport.jquery.plugin/master/tableExport.js',
// 			'assets/bootstrap-table/src/extensions/editable/bootstrap-table-editable.js',
// 			'http://rawgit.com/vitalets/x-editable/master/dist/bootstrap3-editable/js/bootstrap-editable.js'
// 	],
// 	eachSeries = function (arr, iterator, callback) {
// 		callback = callback || function () {};
// 		if (!arr.length) {
// 			return callback();
// 		}
// 		var completed = 0;
// 		var iterate = function () {
// 			iterator(arr[completed], function (err) {
// 				if (err) {
// 					callback(err);
// 					callback = function () {};
// 				}
// 				else {
// 					completed += 1;
// 					if (completed >= arr.length) {
// 						callback(null);
// 					}
// 					else {
// 						iterate();
// 					}
// 				}
// 			});
// 		};
// 		iterate();
// 	};
// 	eachSeries(scripts, getScript, initTable);
// });


// function getScript(url, callback) {
// 	var head = document.getElementsByTagName('head')[0];
// 	var script = document.createElement('script');
// 	script.src = url;
// 	var done = false;
// 	// Attach handlers for all browsers
// 	script.onload = script.onreadystatechange = function() {
// 		if (!done && (!this.readyState ||
// 				this.readyState == 'loaded' || this.readyState == 'complete')) {
// 			done = true;
// 			if (callback)
// 				callback();
// 			// Handle memory leak in IE
// 			script.onload = script.onreadystatechange = null;
// 		}
// 	};
// 	head.appendChild(script);
// 	// We handle everything using the script element injection
// 	return undefined;
// }


