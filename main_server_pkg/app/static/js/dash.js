$(document).ready(main());

function add(){

    $.ajax({
        url: "add_node",
        method: "POST"
    }).done(function(response){
        $("#request-container")[0].innerHTML = `New Authentication Key: ${response.auth_key}`;
    });
    
}

function eventSetup(){
    $("#add_node")[0].addEventListener("click",add);
    
    $("#list_all_nodes")[0].addEventListener("click", function(){
        $("#request-container").load("node_management");
    });
    
    $("#app-list")[0].addEventListener("click", function(){
        $("#request-container").load("app_list_mgmt")
    });
}

function main(){
    eventSetup()
    
}