$(document).ready(main());

function add(){

    $.ajax({
        url: "add_node",
        method: "POST"
    }).done(function(response){
        $("#auth_code_result")[0].innerHTML = `New Authentication Key: ${response.auth_key}`;
    });
    
}

function main(){
    $("#add_node")[0].addEventListener("click",add);
    
}