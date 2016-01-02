var musicDiv = document.getElementById("Music");
var programmingDiv = document.getElementById("Programming");
var otherDiv = document.getElementById("Other");
console.log(musicDiv);
var SubHeads = document.getElementsByClassName("SubHeading");
var mouseheadershow = function(div) {
    console.log("ok");
    var divs = div.getElementsByClassName("SubHeading");
    for (var c = 0; c < divs.length; c++) {
        console.log(divs[c].getAttribute("visibility"));
        divs[c].style.display="block";
    }
}
var mouseheaderhide = function(div) {
    var divs = div.getElementsByClassName("SubHeading");
    for (var c = 0; c < divs.length; c++) {
        divs[c].style.display="none";
    }
}
function setheader(div) {
    div.onmouseover = function() {mouseheadershow(div)};
    div.onmouseleave = function() {mouseheaderhide(div)};
}
for (var c = 0; c < SubHeads.length; c++) {
    SubHeads[c].style.display="none";
    setheader(SubHeads[c]);
}
setheader(musicDiv);
setheader(programmingDiv);
setheader(otherDiv);
