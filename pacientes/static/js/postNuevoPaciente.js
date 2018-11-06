//$('.datepicker').datepicker({maxDate: 'today'});

function base64ToBlob(base64, mime) {
    mime = mime || '';
    var sliceSize = 1024;
    var byteChars = window.atob(base64);
    var byteArrays = [];

    for (var offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
        var slice = byteChars.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    return new Blob(byteArrays, { type: mime });
}

$('#submit').on('click', () => {
    if (fotoTomada) {
        var url = window.location.href
        var image = photo
        var base64ImageContent = image.replace(/^data:image\/(png|jpg);base64,/, "");
        var blob = base64ToBlob(base64ImageContent, 'image/png');

        formData = new FormData();
        formData.append('cedula', document.getElementById('id_cedula').value);
        formData.append('primer_nombre', document.getElementById('id_primer_nombre').value);
        formData.append('segundo_nombre', document.getElementById('id_segundo_nombre').value);
        formData.append('primer_apellido', document.getElementById('id_primer_apellido').value);
        formData.append('segundo_apellido', document.getElementById('id_segundo_apellido').value);
        formData.append('direccion', document.getElementById('id_direccion').value);
        formData.append('ciudad', document.getElementById('id_ciudad').value);
        formData.append('fecha_nacimiento', document.getElementById('id_fecha_nacimiento').value);
        formData.append('estado_civil', document.getElementById('id_estado_civil').value);
        formData.append('telefono', document.getElementById('id_telefono').value);
        formData.append('sexo', document.getElementById('id_sexo').value);
        formData.append('foto', blob, document.getElementById('id_cedula').value.concat('-foto','.png'));
        
        $.ajax({
            url: url,
            type: "POST",
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
        }).done(function (e) {
            $('#ajax-modal').modal('show');
            setInterval(() =>{
                let redireccion = url.replace('/nuevo', '');
                location.href = redireccion;
            },3000);
        });
    } else {
        alert('Es obligatorio tomar la foto');
    }
});


