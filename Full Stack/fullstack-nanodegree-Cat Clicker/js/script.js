var catFaceCounter = 1;
var normalCat = "Normal cat";
var curious = "Curious cat";

$('#cat-title-1').append(normalCat);
$('#cat-title-2').append(curious);

$('#cats').click(function(e) {
    alert("you clicked the cat face " + catFaceCounter + " times.");
    catFaceCounter++;
});
