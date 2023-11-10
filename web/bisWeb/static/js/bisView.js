

function onSelectBossItem(itemName){
    // Realizar la consulta
    var playersOfItem = bossJson.flatMap(function(boss) {
        return boss.items.filter(function(item) {
            return item.name === itemName;
        });
    }).map(function(item) {
        return item.players;
    })[0];

    console.log(playersOfItem);

    var playerListHtml = "";    
    
    // Verificar si se encontraron players
    if (playersOfItem) {
        // Recorrer la lista de items y acceder a sus nombres
        for (var i = 0; i < playersOfItem.length; i++) {
            var playerName = playersOfItem[i].name;
            playerListHtml +=  "<div data-name=\""+playerName+"\" class=\"player\">"+ playerName +"</div>";   
        }

        $("#playerList").html(playerListHtml);       

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
    
    console.log(itemsOfBoss);

    var itemListHtml = "";    
    
    // Verificar si se encontraron items
    if (itemsOfBoss) {
        // Recorrer la lista de items y acceder a sus nombres
        for (var i = 0; i < itemsOfBoss.length; i++) {
            var itemName = itemsOfBoss[i].name;
            itemListHtml +=  "<div data-name=\""+itemName+"\" class=\"item\">"+ itemName +"</div>";   
        }

        $("#itemList").html(itemListHtml);

        //Add click detection
        $(".item").click(function() {
            
            var itemName = $(this).data("name");
            if(currentItemSelected != null){
                $(currentItemSelected).removeClass("selected");
            }
            $(this).addClass("selected");
            currentItemSelected = this;
            
            onSelectBossItem(itemName);
        });

    } else {
        $("#itemList").html("");
    }
}


function loadRaidData(json){
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



var currentBossSelected = null;
var currentItemSelected = null;
var bossJson;

$(document).ready(function() {
    //Parse Json
    var tempElement = document.createElement('div');
    tempElement.innerHTML = bossesJsonString;  
    var decodedString = tempElement.textContent;  
    tempElement.remove();
    bossJson = JSON.parse(decodedString);

    //Load data
    $("#bossList").html("");
    $("#itemList").html("");
    $("#playerList").html("");
    loadRaidData(bossJson);   

});

