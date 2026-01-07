$(document).on("submit", "#incidentForm", function(event) {
    url = $(this).attr("action");
    event.preventDefault();
    // Check if privacy policy checkbox is checked
    if (!$("#consent_checkbox").is(":checked")) {
        Swal.fire({
            icon: 'warning',
            title: 'Aviso',
            html: 'Debe aceptar la política de privacidad para continuar.'
        });
        return;
    }
    $.ajax({
        url: url,
        type: "POST",
        data: $(this).serialize(),
        success: function(response) {
            $("#successMessage").removeClass("hidden");
            $("#incidentForm")[0].reset();
            // SweetAlert message, when it's closed, then successMessage is faded out. Three buttons, Download Parte, Download Talon, Close

            json_response = response;
            url_parte = json_response.url_parte;
            url_talon = json_response.url_talon;

            let html_content = '<p>Gracias por enviar el formulario. Hemos recibido su información correctamente.<br><br> Hemos enviado un correo electrónico de confirmación a la dirección proporcionada.</p>';
            if (url_parte) {
                html_content += `<p> En dicho correo encontrará un enlace para descargar el parte de lesiones.</p>`;
            }
            if (url_talon) {
                html_content += `<p> En dicho correo encontrará un enlace para descargar el talón de pago.</p>`;
            }

            Swal.fire({
                icon: 'success',
                title: 'Formulario enviado',
                html: html_content || 'Gracias por enviar el formulario. Hemos recibido su información correctamente.'
            }).then(() => {
                $("#successMessage").fadeOut(5000);
            });
        },
        error: function(xhr, errmsg, err) {
            console.log("Error submitting form: " + errmsg);
            // SweetAlert message
            json_response = JSON.parse(xhr.responseText);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                html:  json_response.html || 'Ha ocurrido un error al enviar el formulario. Por favor, inténtalo de nuevo más tarde.'
            });
        }
    });
});

$(document).on("click", "#privacy_policy_link", function() {
    // Show SweetAlert with privacy policy content
    Swal.fire({
        title: 'Política de Privacidad',
        html: $('#privacy_policy_content').html(),
        width: '900px',
        confirmButtonText: 'Cerrar'
    });
});

// Funcion que al seleccionar un archivo en el input file, envie el formulario automaticamente
$(document).ready(function() {
    $("#zip-file-input").on("change", function() {
    form = $(this).closest("form");
    // Send form with ajax and post
    $.ajax({
        url: form.attr("action"),
        type: "POST",
        data: new FormData(form[0]),
        processData: false,
        contentType: false,
        success: function(response) {
            $("#successMessage").removeClass("hidden");
            form[0].reset();
            setTimeout(function() {
                $("#successMessage").addClass("hidden");
            }, 2000);
        },
        error: function(xhr, errmsg, err) {
            console.log("Error uploading file: " + errmsg);
            $('#errorMessage').removeClass("hidden");
            form[0].reset();
            setTimeout(function() {
                $("#errorMessage").addClass("hidden");
            }, 2000);
   
        }
    });
    })
});