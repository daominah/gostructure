// this func assumes all elements in input array are maps with same keys,
// returns an <tbody> that has the first row is map keys, remaining rows are data,
// an HTML <table> can call appendChild to use the <tbody>
function convertArrayToTbody(array) {
	if (array.length < 1) {
		console.log("empty data:", array);
		return
	}
	let keys = Object.keys(array[0]);
	let tbody = document.createElement("tbody");
	for (let row = 0; row < keys.length; row++) {
		let key = keys[row];
		let tr = document.createElement("tr");
		let bold = document.createElement("strong");
		bold.appendChild(document.createTextNode(key));
		let tdKey = document.createElement("td");
		tdKey.appendChild(bold);
		tr.appendChild(tdKey);
		for (let col = 0; col < array.length; col++) {
			let td = document.createElement("td");
			let value = array[col][key];
			if (!value) {
				tr.appendChild(td);
				continue
			}
			td.appendChild(document.createTextNode(value));
			tr.appendChild(td)
		}
		tbody.appendChild(tr);
	}
	return tbody
}


window.onload = () => {
	let table = document.getElementById("table0");
	let dataResultFromAPI = [
		{"User": "Tung", "BirthYear": 1991},
		{"User": "Tham", "BirthYear": 2000},
	]
	table.innerHTML = "";
	table.appendChild(convertArrayToTbody(dataResultFromAPI));
};
