document.getElementById("post").addEventListener("click",post_func);
document.getElementById("get").addEventListener("click",get_func);

function post_func(){
	var data = $('#posts_data').val();
	console.log("post "+data);
	$.post('../apiTester',JSON.stringify({'url':data,'req':'POST'}),function(resp){
		console.log(resp);
	},'json')
}

function get_func(){
	var data = $('#posts_data').val();

	console.log("get "+data);
	$.post('../apiTester',JSON.stringify({url:data,'req':'GET'}),function(resp){
		console.log(resp);
	},'json')
}

function bs(){
	$.post('../apiTester',JSON.stringify({val:'test','req':'POST'}),function(resp){
		console.log(resp);
	},'json')
}