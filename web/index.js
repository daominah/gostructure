// this func assumes all elements in input array are maps with same keys,
// this returns an <tbody> that has the first row is map keys, remaining rows are data rows,
// an HTML <table> can call appendChild to use the returned <tbody>
// If array is empty or null, returns tbody with single "No data" cell
function convertArrayToTbody(array) {
	let tbody = document.createElement("tbody");

	if (!array || array.length < 1) {
		// Display "No data" message
		let tr = document.createElement("tr");
		let td = document.createElement("td");
		td.setAttribute("colspan", "100");
		td.style.textAlign = "center";
		td.appendChild(document.createTextNode("No data"));
		tr.appendChild(td);
		tbody.appendChild(tr);
		return tbody;
	}

	let keys = Object.keys(array[0]);

	// Create header row
	let headerRow = document.createElement("tr");
	for (let i = 0; i < keys.length; i++) {
		let th = document.createElement("th");
		th.appendChild(document.createTextNode(keys[i]));
		headerRow.appendChild(th);
	}
	tbody.appendChild(headerRow);

	// Create data rows
	for (let row = 0; row < array.length; row++) {
		let tr = document.createElement("tr");
		for (let col = 0; col < keys.length; col++) {
			let td = document.createElement("td");
			let value = array[row][keys[col]];
			if (value !== null && value !== undefined) {
				td.appendChild(document.createTextNode(value));
			}
			tr.appendChild(td);
		}
		tbody.appendChild(tr);
	}
	return tbody;
}

window.onload = () => {
	let table = document.getElementById("table0");

	// fetch data from the server API,
	// the URL is relative to the web page location,
	// so requires server to serve both web and API on the same host to work correctly
	fetch("/api/v1/product?query=")
		.then(response => {
			if (!response.ok) {
				throw new Error("API request failed");
			}
			return response.json();
		})
		.then(products => {
			table.innerHTML = "";
			let tbody = convertArrayToTbody(products);
			table.appendChild(tbody);
		})
		.catch(error => {
			console.log("error GET /api/v1/product:", error);
			table.innerHTML = "";
			let tbody = convertArrayToTbody(null);
			table.appendChild(tbody);
		});
};
