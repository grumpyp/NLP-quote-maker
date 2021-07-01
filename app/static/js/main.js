
function validateForm(text) {
    textArr = text.value.split(" ")
    document.getElementById("result").style.display = "block";
	if (textArr.length < 4) {
		alert("Please input an sentence");
		return false;
    }    
}