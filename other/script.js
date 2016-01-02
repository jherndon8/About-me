var difficulties = {
    beginner: {
        width: 9,
        height: 9,
        mines: 10
    },
    medium: {
        width: 16,
        height: 16,
        mines: 40
    },
    expert: {
        width: 30,
        height: 16,
        mines: 99
    }
}

var difficulty = difficulties.medium;
var grid = document.getElementById("grid");

function cell(y, x) {
    var a = grid;
    return grid.children[y].children[x];
}

addMines = function(event) {
    y = event.srcElement.row;
    x = event.srcElement.col;
    //console.log(event);
    console.log("First click at " + y + "th row and " + x + "th column");
    for (var y = 0; y < difficulty.height; y++) {
        for (var x = 0; x < difficulty.width; x++) {
            cell(y, x).onclick = function(evnt) {clickCell(evnt)};
        }
    }
    for (var mines = 0; mines < difficulty.mines;) {
        var ygen = Math.floor(Math.random() * difficulty.height);
        var xgen = Math.floor(Math.random() * difficulty.width);
        if ((Math.abs(y - ygen) > 1 || Math.abs(x - xgen) > 1)
            && !cell(ygen, xgen).classList.contains("mine")) {
            cell(ygen, xgen).classList.add("mine");
            mines++;
        }
    }
}

clickCell = function(event) {
    y = event.srcElement.row;
    x = event.srcElement.col;
    console.log("Clicking cell at row " + y + ", column " + x);
    //TODO
}

function hardResetBoard() {
    grid.innerHTML = "" //Non-standard, but fast and well supported?
    grid.style.width = 20 * difficulty.width;
    grid.style.height = 20 * difficulty.height;
    for (var y = 0; y < difficulty.height; y++) {
        var row = document.createElement("div");
        var classAtt = document.createAttribute("class");
        classAtt.value = "row";
        row.setAttributeNode(classAtt);
        for (var x = 0; x < difficulty.width; x++) {
            var classAtt2 = document.createAttribute("class");
            var cur = document.createElement("div");
            classAtt2.value = "cell";
            cur.setAttributeNode(classAtt2);
            cur.row = y;
            cur.col = x;
            cur.onclick = function() {addMines(event)};
            row.appendChild(cur);
        }
        grid.appendChild(row);
    }
}


hardResetBoard();
