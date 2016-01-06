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
var colors = ["transparent", "blue", "green", "red", "violet", "magenta", "cyan", "black", "grey"];
var difficulty = difficulties.beginner;
var grid = document.getElementById("grid");
var clickedCount;
var gameOverFlag = false;
var postGame = document.getElementById("postGame");
var buttons = document.getElementsByTagName("Button");
for (var b = 0; b < buttons.length; b++) {
    buttons[b].onclick = function(event) {
        difficulty = difficulties[event.srcElement.id];
        hardResetBoard();
    };
}


function cell(y, x) {
    if (y < 0 || y >= difficulty.height || x < 0 || x >= difficulty.width) {
        return null;
    }
    return grid.children[y].children[x];
}

addMines = function(event) {
    y = event.srcElement.row;
    x = event.srcElement.col;
    //console.log(event);
    console.log("First click at " + y + "th row and " + x + "th column");
    for (var i = 0; i < difficulty.height; i++) {
        for (var j = 0; j < difficulty.width; j++) {
            cell(i, j).onclick = function(evnt) {clickCell(evnt)};
            cell(i, j).oncontextmenu = function(evnt) {return rightClickCell(evnt)};
            cell(i, j).ondblclick = function(evnt) {dblclickCell(evnt)};
        }
    }
    for (var mines = 0; mines < difficulty.mines;) {
        var ygen = Math.floor(Math.random() * difficulty.height);
        var xgen = Math.floor(Math.random() * difficulty.width);
        if ((Math.abs(y - ygen) > 1 || Math.abs(x - xgen) > 1)
            && !cell(ygen, xgen).classList.contains("mine")) {
            cell(ygen, xgen).classList.add("mine");
            mines++;
            //Good for debugging
            //cell(ygen, xgen).style.backgroundColor = "#DD0000";
        }
    }
    calculateAdjacencies();
    clickCell(event);
}

function isMine(y, x) {
    return cell(y, x).classList.contains("mine");
}

function calculateAdjacencies() {
    for (var y = 0; y < difficulty.height; y++) {
        for (var x = 0; x < difficulty.width; x++) {
            var count = 0;
            var c = cell(y, x);
            for (var yy = -1; yy <= 1; yy++) {
                for (var xx = -1; xx <= 1; xx++) {
                    var cur = cell(y+yy, x+xx);
                    if (cur != null && cur.classList.contains("mine")) {
                        count++;
                    }
                }
            }
            c.adjCount = count;
            c.innerHTML = count;
            c.style.color = "transparent";
        }
    }
}

clickCell = function(event) {
    if (postGame.innerHTML != ""
            || event.srcElement.classList.contains("clicked")
            || event.srcElement.classList.contains("mark")) {return;}
    var y = event.srcElement.row;
    var x = event.srcElement.col;
    if (isMine(y, x)) {
        gameOver(false);
        return;
    }
    clickedCount++;
    cell(y, x).classList.add("clicked");
    console.log("Clicking cell at row " + y + ", column " + x);
    cell(y, x).style.color = colors[cell(y, x).adjCount];
    if (cell(y, x).adjCount === 0) {
        for (var yy = -1; yy <= 1; yy++) {
            for (var xx = -1; xx <= 1; xx++) {
                if ((xx != 0 || yy != 0) && cell(yy+y, xx+x) != null) {
                    cell(yy+y, xx+x).click();
                }
            }
        }
    }
    if (clickedCount == difficulty.height * difficulty.width - difficulty.mines) {
        gameOver(true);
    }
}

rightClickCell = function(event) {
    if (postGame.innerHTML != "") return;
    var y = event.srcElement.row;
    var x = event.srcElement.col;
    console.log("Right Clicking cell at row " + y + ", column " + x);
    if (!cell(y, x).classList.contains("clicked")) {
        if (cell(y, x).classList.contains("mark")) {
            cell(y, x).classList.remove("mark");
        } else {
            cell(y, x).classList.add("mark");
        }
    }
    return false;
}

dblclickCell = function(event) {
    var clicked = event.srcElement;
    if (!clicked.classList.contains("clicked")) {
        return;
    }
    var y = event.srcElement.row;
    var x = event.srcElement.col;
    var count = 0;
    for (var yy = -1; yy <= 1; yy++) {
        for (var xx = -1; xx <= 1; xx++) {
            var c = cell(y + yy, x + xx);
            if (c != null && c.classList.contains("mark")) {
                count++;
            }
        }
    }
    if (count != clicked.innerHTML) {
        return;
    }
    console.log("double clicking " + y + ", " + x);
    for (var yy = -1; yy <= 1; yy++) {
        for (var xx = -1; xx <= 1; xx++) {
            var c = cell(y + yy, x + xx);
            if (c != null) {
                c.click();
            }
        }
    }
}

function hardResetBoard() {
    postGame.innerHTML = "";
    grid.innerHTML = ""; //Non-standard, but fast and well supported?
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
    clickedCount = 0;
}

function gameOver(won) {
    if (postGame.innerHTML != "") return;
    var mines = document.getElementsByClassName("mine");
    for (var a = 0; a < mines.length; a++) {
        mines[a].style.backgroundColor = "#AA0000";
    }
    if (won) {
        postGame.innerHTML = "Congratulations, you won!"
    } else {
        postGame.innerHTML = "Sorry, you lost"
    }
}

function win() {
    console.log("You won");
}

hardResetBoard();
