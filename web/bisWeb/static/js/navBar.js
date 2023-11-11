
$(document).ready(function () {
    // Clic en el botón de inicio de sesión
    $("#loginForm").submit(function (event) {
        // Detener el envío del formulario predeterminado
        event.preventDefault();
       
        // Envía el formulario
        this.submit();
    });
    //Clic en logout
    $("#salirSesionButton").click(function () {
       
        window.location.href = '/bisWeb/logout'; 
    });
    //Clic en panel de control
    $("#panelControlButton").click(function () {
       
        window.location.href = '/bisWeb/adminPanel'; 
    });
    //Clic en lista items
    $("#bisViewButton").click(function () {
       
        window.location.href = '/bisWeb/bisListView'; 
    });
});
