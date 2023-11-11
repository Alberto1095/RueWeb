
$(document).ready(function () {

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


    $("#itemsUploadForm").submit(function (e) {
        e.preventDefault();    
        var formData = new FormData();
        var fileInput = document.getElementById('fileItemsUpload');
        formData.append('excelFile', fileInput.files[0]);

        $.ajax({
            url: '/bisWeb/initializeDatabase',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                // Manejar la respuesta exitosa
                console.log(data);
                if(data.success){
                    alert('Actualizado correctamente!');
                }else{
                    alert('¡Error al subir el fichero!');
                }
            },
            error: function (error) {
                // Manejar errores
                console.log(error);
                alert('¡Error al subir el fichero!');
            }
        });

    });
    $("#playerBisesUploadForm").submit(function (e) {
        e.preventDefault();    
        var formData = new FormData();
        var fileInput = document.getElementById('filePlayerBisesUpload');
        formData.append('excelFile', fileInput.files[0]);

        $.ajax({
            url: '/bisWeb/initializePlayerItems',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                // Manejar la respuesta exitosa
                console.log(data);
                if(data.success){
                    alert('Actualizado correctamente!');
                }else{
                    alert('¡Error al subir el fichero!');
                }
            },
            error: function (error) {
                // Manejar errores
                console.log(error);
                alert('¡Error al subir el fichero!');
            }
        });
    });
    
    $("#borrarBaseDatosButton").click(function (e) { 
        e.preventDefault();
        var confirmacion = confirm("¿Estás seguro de que quieres borrar toda la base de datos?");
        if (confirmacion) {
            $.ajax({
                url: '/bisWeb/cleanDatabase',
                type: 'POST',           
                success: function (data) {
                    // Manejar la respuesta exitosa
                    console.log(data);

                    if(data.success){
                        alert('¡Borrado correctamente!');
                    }else{
                        alert('¡Error al borrar la base de datos!');
                    }
                },
                error: function (error) {
                    // Manejar errores
                    console.log(error);
                    alert('¡Error al borrar la base de datos!');
                }
            });
        }
    });
});
