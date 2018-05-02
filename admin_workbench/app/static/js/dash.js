$(document).ready(main());

function eventSetup(){
    $("#add_node")[0].addEventListener("click",function add(){
        $("#request-container").load("add_client");
    });
    
    $("#list_all_nodes")[0].addEventListener("click", function(){
        $("#request-container").load("node_management");
    });
    
    $("#app-list")[0].addEventListener("click", function(){
        $("#request-container").load("app_list_mgmt")
    });
    
    $("#add_server")[0].addEventListener("click", function(){
        $("#request-container").load("add_server")
    });
}

function main(){
    eventSetup()
    
}