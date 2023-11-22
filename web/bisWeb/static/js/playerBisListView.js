
function getAllPlayers() {
    // Inicializar un conjunto para almacenar nombres de jugadores únicos
    let nombresUnicos = new Set();

    // Iterar sobre la lista de bosses en el JSON
    bossJson.forEach(boss => {
        // Iterar sobre la lista de items para cada boss
        boss.items.forEach(item => {
            // Iterar sobre la lista de players para cada item
            item.players.forEach(player => {
                // Agregar el nombre del jugador al conjunto
                nombresUnicos.add(player.name);
            });
        });
    });

    // Convertir el conjunto a un array y devolverlo
    return Array.from(nombresUnicos).sort();
}

function getBossesForPlayer(playerName){
    let bosses = [];

    // Iterar sobre la lista de bosses en el JSON
    bossJson.forEach(boss => {
        // Iterar sobre la lista de items para cada boss
        boss.items.forEach(item => {
            // Verificar si el jugador está presente en la lista de players para el item
            if (item.players.some(player => player.name === playerName)) {
                // Agregar el nombre del boss a la lista de bosses si aún no está presente
                if (!bosses.includes(boss.name)) {
                    bosses.push(boss.name);
                }
            }
        });
    });

    return bosses;
}

function getItemsForPlayerInBoss(bossName,playerName){
    let itemsDelJugador = [];

    // Buscar el boss en el JSON por nombre
    let bossEncontrado = bossJson.find(boss => boss.name === bossName);

    // Si se encontró el boss, buscar los items para el jugador
    if (bossEncontrado) {
        bossEncontrado.items.forEach(item => {
            // Verificar si el jugador está presente en la lista de players para el item
            if (item.players.some(player => player.name === playerName)) {
                // Agregar el nombre del item a la lista de items del jugador
                if (!itemsDelJugador.includes(item.name)) {
                    itemsDelJugador.push(item.name);
                }               
            }
        });
    }

    return itemsDelJugador;
}



function onSelectBoss(bossName,playerName){    
    var itemList = getItemsForPlayerInBoss(bossName,playerName)      

    var itemListHtml = "";  
    
    // Verificar si se encontraron items
    if (itemList.length > 0) {
        // Recorrer la lista de items y acceder a sus nombres
        for (var i = 0; i < itemList.length; i++) {
            var itemName = itemList[i];           
            itemListHtml +=  "<div data-name=\""+itemName+"\" class=\"item\">"+ itemName +"</div>";   
        }

        $("#itemList").html(itemListHtml);         

    } else {
        $("#itemList").html("");
    }
}

function onSelectPlayer(playerName){
    //Mostrar bosses que tiene el jugador
    var bossesList = getBossesForPlayer(playerName)      
    $("#bossList").html("");
    var bossListHtml = "";    
    
    // Verificar si se encontraron items y añadirlos a la lista
    if (bossesList.length > 0) {
        // Recorrer la lista de items y acceder a sus nombres
        for (var i = 0; i < bossesList.length; i++) {
            var bossName = bossesList[i];           
            bossListHtml +=  "<div data-player=\""+playerName+"\" data-name=\""+bossName+"\" class=\"boss\">"+ bossName +"</div>";   
        }
        
        $("#bossList").html(bossListHtml);

        //Add click detection
        $(".boss").click(function() {            
            var bossName = $(this).data("name");
            var playername = $(this).data("player");
            if(currentBossSelected != null){
                $(currentBossSelected).removeClass("selected");
            }
            $(this).addClass("selected");
            currentBossSelected = this;
            
            onSelectBoss(bossName,playerName);
        });

    } else {
        $("#bossList").html("");
    }
}


function loadData(json){
    //Obtener los jugadores que hay
    var playerList = getAllPlayers();
    var playerListHtml = "";    
   
    for (var i = 0; i < playerList.length; i++) {            
        var playerName = playerList[i];
        playerListHtml +=  "<div data-name=\""+playerName+"\" class=\"player\">"+ playerName +"</div>";   
    }

    $("#playerList").html(playerListHtml);
    //Add click detection
    $(".player").click(function() {
        
        var playerName = $(this).data("name");
        if(currentPlayerSelected != null){
            $(currentPlayerSelected).removeClass("selected");
        }
        $(this).addClass("selected");
        currentPlayerSelected = this;
        
        onSelectPlayer(playerName);
    });
}

function initialize(){
    //Parse Json
    var tempElement = document.createElement('div');
    tempElement.innerHTML = bossesJsonString;  
    var decodedString = tempElement.textContent;      
    bossJson = JSON.parse(decodedString);    

    tempElement.remove();
    $("#bossList").html("");
    $("#itemList").html("");
    $("#playerList").html("");    
    loadData(bossJson);    
}

var currentBossSelected = null;
var currentPlayerSelected = null;
var bossJson;


$(document).ready(function() {    
    //Initialize
    initialize();
});

