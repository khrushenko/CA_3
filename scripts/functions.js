
function load() {
    //setInterval(function () {
    readLabs();
    //}, 5000)
}


function createLab() {
    var inputName = $('#nameAdd')[0];
    var inputAbout = $('#aboutAdd')[0];
    var inputState = $('#stateAdd')[0];
    var name = inputName.value;
    var about = inputAbout.value;
    var state = inputState.value;
    inputName.value = "";
    inputAbout.value = "";
    inputState.value = "";

    var data = "name=" + name + "&about=" + about + "&state=" + state;

    $.post("/create", data, function () {
        readLabs();
    });

    showResult();
}


function readLabs() {
    $.get("/read", function (data) {
        var labs = JSON.parse(data);
        var table = $("table")[0];

        while (table.rows.length > 1)
            table.deleteRow(table.rows.length - 1);

        for (var i = labs.length - 1; 0 <= i; i--) {
            var name = labs[i]['name'];
            var about = labs[i]['about'];
            var state = labs[i]['state'];

            var newRow = table.insertRow(1);
            var cellName = newRow.insertCell(0);
            cellName.innerHTML = name;
            cellName.className = "TableSimpleCell";
            var cellAbout = newRow.insertCell(1);
            cellAbout.innerHTML = about;
            cellAbout.className = "TableSimpleCell";
            var cellState = newRow.insertCell(2);
            cellState.innerHTML = state;
            cellState.className = "TableSimpleCell";
            var cellButtons = newRow.insertCell(3);
            //var
            cellButtons.innerHTML = '<input type="button" id="'+ name + '" value="Delete" onClick="deleteLab(\'' + name + '\')"/>';
            cellButtons.className = "TableButtonCell";
        }


        var select = $("#nameChange")[0];

        while (select.length > 0)
            select.remove(select.length - 1);

        for (var j = 0; j < labs.length; j++) {
            var option = document.createElement("option");
            var nameOption = labs[j]['name'];
            option.value = nameOption;
            option.text = nameOption;
            select.add(option);
        }
    });
}


function updateLab() {
    var selectName = $('#nameChange')[0];
    var selectField = $('#fieldChange')[0];
    var inputValue = $('#inputUpdate')[0];

    var data = 'name=' + selectName.value + '&field=' + selectField.value + '&value=' + inputValue.value;
    inputValue.value = '';

    $.post("/update", data, function () {
        readLabs();
    });

    showResult();
}


function deleteLab(name) {
    $.post("/delete", name, function () {
        readLabs();
    });

    showResult();
}


function showResult() {
    $.get("/result", function (data) {
        var whatWeGot = JSON.parse(data);

        var resultP = $('.result')[0];
        resultP.innerHTML = whatWeGot['result'];
        resultP.style.color = whatWeGot['color'];

        setTimeout(function () {
            resultP.innerHTML = "";
        }, 5000);
    });
}