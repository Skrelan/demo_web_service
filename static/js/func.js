console.log("I am imported");
document.getElementById("click_me").addEventListener("click",log_response);

function log_response(){
	$.getJSON("/test", function(response){
		console.log(response);
	})};