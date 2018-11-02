// function tieneSoporteUserMedia() {
//     return !!(navigator.getUserMedia || (navigator.mozGetUserMedia || navigator.mediaDevices.getUserMedia) || navigator.webkitGetUserMedia || navigator.msGetUserMedia)
// }

// function _getUserMedia() {
//     return (navigator.getUserMedia || (navigator.mozGetUserMedia || navigator.mediaDevices.getUserMedia) || navigator.webkitGetUserMedia || navigator.msGetUserMedia).apply(navigator, arguments);
// }


// if (tieneSoporteUserMedia()) {
//     // Declaramos elementos del DOM
// var videoVar = document.getElementById("video"),
// $canvas = document.getElementById("canvas"),
// $boton = document.getElementById("boton"),
// $estado = document.getElementById("estado");
//     _getUserMedia({
//             video: true
//         },
//         function(stream) {
//             console.log("Permiso concedido");
//             videoVar.srcObject = stream;
//             videoVar.play();

//             //Escuchar el click
//             $boton.addEventListener("click", function() {

//                 //Pausar reproducción
//                 videoVar.pause();

//                 //Obtener contexto del canvas y dibujar sobre él
//                 var contexto = $canvas.getContext("2d");
//                 $canvas.width = videoVar.videoWidth;
//                 $canvas.height = videoVar.videoHeight;
//                 contexto.drawImage(videoVar, 0, 0, $canvas.width, $canvas.height);

//                 var foto = $canvas.toDataURL(); //Esta es la foto, en base 64
//                 $estado.innerHTML = "Enviando foto. Por favor, espera...";
//                 var xhr = new XMLHttpRequest();
//                 xhr.open("POST", "./guardar_foto.php", true);
//                 xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//                 xhr.send(encodeURIComponent(foto)); //Codificar y enviar

//                 xhr.onreadystatechange = function() {
//                     if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
//                         console.log("La foto fue enviada correctamente");
//                         console.log(xhr);
//                         $estado.innerHTML = "Foto guardada con éxito. Puedes verla <a target='_blank' href='./" + xhr.responseText + "'> aquí</a>";
//                     }
//                 }

//                 //Reanudar reproducción
//                 videoVar.play();
//             });
//         },
//         function(error) {
//             console.log("Permiso denegado o error: ", error);
//             $estado.innerHTML = "No se puede acceder a la cámara, o no diste permiso.";
//         });
// } else {
//     alert("Lo siento. Tu navegador no soporta esta característica");
//     $estado.innerHTML = "Parece que tu navegador no soporta esta característica. Intenta actualizarlo.";
// }
(function() {

    var streaming = false,
        video        = document.querySelector('#video'),
        canvas       = document.querySelector('#canvas'),
        photo        = document.querySelector('#photo'),
        startbutton  = document.querySelector('#startbutton'),
        width = 320,
        height = 0;
  
    navigator.getMedia = ( navigator.getUserMedia ||
                           navigator.webkitGetUserMedia ||
                           navigator.mozGetUserMedia ||
                           navigator.msGetUserMedia);
  
    navigator.getMedia(
      {
        video: true,
        audio: false
      },
      function(stream) {
        if (navigator.mozGetUserMedia) {
          video.mozSrcObject = stream;
        } else {
          var vendorURL = window.URL || window.webkitURL;
          video.srcObject = stream;
        }
        video.play();
      },
      function(err) {
        console.log("An error occured! " + err);
      }
    );
  
    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);
  
    function takepicture() {
      canvas.width = width;
      canvas.height = height;
      canvas.getContext('2d').drawImage(video, 0, 0, width, height);
      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
    }
  
    startbutton.addEventListener('click', function(ev){
        takepicture();
      ev.preventDefault();
    }, false);
  
  })();
