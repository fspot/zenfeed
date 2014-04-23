(function(){
	var elems = document.getElementById('feeds') || document.getElementById('entries');
	elems.addEventListener('click', function (e) {
			var gridRow = e.target;
			if (gridRow.tagName === "A") { return; }
			if (! gridRow.classList.contains("grid-row")) { gridRow = gridRow.parentNode; }
			document.location.href = gridRow.dataset.url;
		}, false
	);
})();
