console.log("I am imported");
document.getElementById("nxt").addEventListener("click",load_content);


function log_response(){
	$.getJSON("/test", function(response){
		console.log(response);
	})};

function update_holders(input){
	for(var i = 0; i<input.length;i++){
		console.log(input[i]);
		var image =  document.getElementById('img_'+String(i));
		var data = document.getElementById('stats_'+String(i));
		var button = document.getElementById('button_'+String(i));
		image.setAttribute("src",input[i].image_url);
		image.style.width = 150;
		image.style.height = 150;
	}
}

function load_content(){
	$.post('/products',JSON.stringify({'requested by':'Javascript'}),function(resp){
		console.log(resp);
		update_holders(resp.result);
	},'json')
}

