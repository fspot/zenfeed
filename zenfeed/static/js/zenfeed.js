(function(){
	// onclick handling
	var elems = document.getElementById('feeds') || document.getElementById('entries');
	if (elems != null) elems.addEventListener('click', function (e) {
		var gridRow = e.target;
		if (gridRow.nodeName === "A") return;
		if (! gridRow.classList.contains("grid-row")) gridRow = gridRow.parentNode;
		if (gridRow.dataset.url) document.location.href = gridRow.dataset.url;
	}, false);

	// keyboard navigation
	var onEntryPage = null !== document.getElementById('entry');
	var scrollElem = (function () {
		if (document.body.scrollTopMax === 0) return document.documentElement;
		else return document.body;
	})();
	function focusFirst() { document.querySelector('.navlink a').focus(); }
	function getLinks() {
		if (! window.navLinks) window.navLinks = [].slice.call(document.querySelectorAll('.navlink a'));
		return window.navLinks;
	}
	document.addEventListener("keypress", function (e) {
		switch (String.fromCharCode(e.charCode)) {
			case "z":
			case "w":
				if (onEntryPage) { scrollElem.scrollTop -= 50; break; }
				if (document.activeElement.nodeName !== "A") { focusFirst(); break; }
				var actualIndex = getLinks().indexOf(document.activeElement);
				if (actualIndex > 0) getLinks()[actualIndex-1].focus();
				break;
			case "s":
				if (onEntryPage) { scrollElem.scrollTop += 50; break; }
				if (document.activeElement.nodeName !== "A") { focusFirst(); break; }
				var actualIndex = getLinks().indexOf(document.activeElement);
				if (actualIndex < getLinks().length-1) getLinks()[actualIndex+1].focus();
				break;
			case "q":
			case "a":
				window.history.go(-1);
				break;
			case "d":
				if (document.activeElement.nodeName === "A")
					document.location.href = document.activeElement.href;
				break;
			case "o":
				// "o"pen this url
				var link = document.getElementById('article-link');
				document.location.href = link;
				break;
		}
	}, false);
})();
