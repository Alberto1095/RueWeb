
function searchPlayerHasPickedItem(playerId, bossItemId) {
    for (const itemPicked of itemsPickedJson) {
      if (itemPicked.player === playerId && itemPicked.bossItem === bossItemId) {
        // Si se encuentra la combinación de player y bossItem, devolver un objeto con itemLevel y bossItem
        return {
          itemLevel: itemPicked.itemLevel,
          exist: true
        };
      }
    }  
    // Si no se encuentra la combinación, devolver un objeto con ambas variables como null
    return {
        itemLevel: 0,
        exist: false
    };
}

function updatePlayerList(itemsPickedJsonString){
    itemsPickedJson = JSON.parse(itemsPickedJsonString);
    var itemId = $(currentItemSelected).data("id");  
    // Realizar la consulta
    var playersOfItem = bossJson.flatMap(function(boss) {
        return boss.items.filter(function(item) {
            return item.id === itemId;
        });
    }).map(function(item) {
        return item.players;
    })[0];   

    var playerListHtml = "";
    $("#pickItemContainer").addClass("hide");      
    
    // Verificar si se encontraron players
    if (playersOfItem) {
        // Recorrer la lista de items y acceder a sus nombres
        for (var i = 0; i < playersOfItem.length; i++) {
            var playerName = playersOfItem[i].name;   
            var playerId = playersOfItem[i].id;   
            var resultData = searchPlayerHasPickedItem(playerId,itemId);
            
            if(resultData.exist){
                playerListHtml +=  "<div data-item=\""+itemId+"\" data-id=\""+playerId+"\" data-name=\""+playerName+"\" class=\"player hasItem\">"+ playerName +" - "+resultData.itemLevel +"</div>";   
            }else{
                playerListHtml +=  "<div data-item=\""+itemId+"\" data-id=\""+playerId+"\" data-name=\""+playerName+"\" class=\"player\">"+ playerName +"</div>";   
            }       
        }

        $("#playerList").html(playerListHtml);        
        
        //Add click detection
        $(".player").click(function() {
            
            var playerName = $(this).data("name");
            var playerId = $(this).data("id");
            var itemId = $(this).data("item");
            
            if(currentPlayerSelected != null){
                $(currentPlayerSelected).removeClass("selected");
            }
            $(this).addClass("selected");
            currentPlayerSelected = this;
            
            onSelectPlayer(playerId,itemId);
            
        });


    } else {
        $("#playerList").html("");
    }

}

function onSelectPlayer(playerId,itemId){    
    if(loggedAsAdmin=="True"){        
        $("#pickItemContainer").removeClass("hide");

        //Check if player has item to enable delete button
        var hasItem = itemsPickedJson.some(item => item.player === playerId && item.bossItem === itemId);
        
        if(hasItem){           
            $("#removeItem").removeClass("hide");
        }else{            
            $("#removeItem").addClass("hide");
        }
    }
}

function onSelectBossItem(itemName,itemId){
    // Realizar la consulta
    var playersOfItem = bossJson.flatMap(function(boss) {
        return boss.items.filter(function(item) {
            return item.name === itemName;
        });
    }).map(function(item) {
        return item.players;
    })[0];   

    var playerListHtml = "";
    $("#pickItemContainer").addClass("hide");      
    
    // Verificar si se encontraron players
    if (playersOfItem) {
        // Recorrer la lista de items y acceder a sus nombres
        for (var i = 0; i < playersOfItem.length; i++) {
            var playerName = playersOfItem[i].name;   
            var playerId = playersOfItem[i].id;   
            var resultData = searchPlayerHasPickedItem(playerId,itemId);
            
            if(resultData.exist){
                playerListHtml +=  "<div data-item=\""+itemId+"\" data-id=\""+playerId+"\" data-name=\""+playerName+"\" class=\"player hasItem\">"+ playerName +" - "+resultData.itemLevel +"</div>";   
            }else{
                playerListHtml +=  "<div data-item=\""+itemId+"\" data-id=\""+playerId+"\" data-name=\""+playerName+"\" class=\"player\">"+ playerName +"</div>";   
            }       
        }

        $("#playerList").html(playerListHtml);        
        
        //Add click detection
        $(".player").click(function() {
            
            var playerName = $(this).data("name");
            var playerId = $(this).data("id");
            var itemId = $(this).data("item");
            
            if(currentPlayerSelected != null){
                $(currentPlayerSelected).removeClass("selected");
            }
            $(this).addClass("selected");
            currentPlayerSelected = this;
            
            onSelectPlayer(playerId,itemId);
           
        });


    } else {
        $("#playerList").html("");
    }
}

function onSelectBoss(bossName){
    //Mostrar items
    var itemsOfBoss = bossJson.filter(function(boss) {
        return boss.name === bossName;
    }).map(function(boss) {
        return boss.items;
    })[0];    
    
    //Clear player list
    $("#playerList").html("");
    $("#pickItemContainer").addClass("hide");

    var itemListHtml = "";    
    
    // Verificar si se encontraron items y añadirlos a la lista
    if (itemsOfBoss) {
        // Recorrer la lista de items y acceder a sus nombres
        for (var i = 0; i < itemsOfBoss.length; i++) {
            var itemName = itemsOfBoss[i].name;
            var itemId = itemsOfBoss[i].id;
            itemListHtml +=  "<div data-id=\""+itemId+"\" data-name=\""+itemName+"\" class=\"item\">"+ itemName +"</div>";   
        }
        
        $("#itemList").html(itemListHtml);

        //Add click detection
        $(".item").click(function() {
            
            var itemName = $(this).data("name");
            var itemId = $(this).data("id");
            if(currentItemSelected != null){
                $(currentItemSelected).removeClass("selected");
            }
            $(this).addClass("selected");
            currentItemSelected = this;
            
            onSelectBossItem(itemName,itemId);
        });

    } else {
        $("#itemList").html("");
    }
}


function loadBossesData(json){
    // Iterar sobre cada boss para generar el html
    var bossListHtml = "";    
   
    for (var i = 0; i < json.length; i++) {
        var boss = json[i];       
        var bossName = boss.name;

        bossListHtml +=  "<div data-name=\""+bossName+"\" class=\"boss\">"+ bossName +"</div>";   
    }

    $("#bossList").html(bossListHtml);
    //Add click detection
    $(".boss").click(function() {
        
        var bossName = $(this).data("name");
        if(currentBossSelected != null){
            $(currentBossSelected).removeClass("selected");
        }
        $(this).addClass("selected");
        currentBossSelected = this;
        
        onSelectBoss(bossName);
    });
}

function initialize(){
    //Parse Json
    var tempElement = document.createElement('div');
    tempElement.innerHTML = bossesJsonString;  
    var decodedString = tempElement.textContent;      
    bossJson = JSON.parse(decodedString);

    tempElement.innerHTML = itemsPickedJsonString;  
    decodedString = tempElement.textContent;  
    itemsPickedJson = JSON.parse(decodedString);

    tempElement.remove();
    $("#bossList").html("");
    $("#itemList").html("");
    $("#playerList").html("");    
    loadBossesData(bossJson); 
    
    $("#addItem").click(function (e) { 
        e.preventDefault();
        
        var playerId = $(currentPlayerSelected).data("id");
        var itemId = $(currentPlayerSelected).data("item");
        var itemLevel = $("#itemLevelInputText").val();
       
        var dataToSend = {
            playerId: playerId,
            itemId: itemId,
            itemLevel: itemLevel
        };
        $.ajax({
            url: '/bisWeb/addOrUpdateItemPicked',
            type: 'POST',
            data: dataToSend,           
            success: function (data) {
                // Manejar la respuesta exitosa
                console.log(data);
                if(data.success) {                    
                    updatePlayerList(data.itemsPickedJson);
                }else{
                    alert('¡Error al establecer item!');
                }
                
            },
            error: function (error) {
                // Manejar errores
                console.log(error);
                alert('¡Error al establecer item!');
            }
        });        
    });

    $("#removeItem").click(function (e) { 
        e.preventDefault();
       
        var playerId = $(currentPlayerSelected).data("id");
        var itemId = $(currentPlayerSelected).data("item");       
        console.log(currentPlayerSelected);
        var dataToSend = {
            playerId: playerId,
            itemId: itemId
        };
        console.log(dataToSend);
        $.ajax({
            url: '/bisWeb/removeItemPicked',
            type: 'POST',
            data: dataToSend,     
            success: function (data) {
                // Manejar la respuesta exitosa
                console.log(data);

                if(data.success) {                    
                    updatePlayerList(data.itemsPickedJson);
                }else{
                    alert('¡Error al borrar item!');
                }             
            },
            error: function (error) {
                // Manejar errores
                console.log(error);
                alert('¡Error al borrar item!');
            }
        });        
    });
}

var currentBossSelected = null;
var currentItemSelected = null;
var currentPlayerSelected = null;
var bossJson;
var itemsPickedJson;

$(document).ready(function() {
    // Función para obtener el valor del token CSRF desde la cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Buscar el nombre del token CSRF en la cookie
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    // Obtener el token CSRF del cookie
    var csrftoken = getCookie('csrftoken');

    // Configurar el token CSRF en la solicitud AJAX
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    //Initialize
    initialize();

});

