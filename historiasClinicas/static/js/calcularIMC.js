function calculaIMC(peso, talla){
    var imc=peso/(talla*talla)
    return imc
}

$(document).ready(function () {
    $("#id_imc").click(function () {
        var talla = $("#id_talla").val();
        var peso = $("#id_peso").val();
        var imc = calculaIMC(peso,talla/100);
        $("#id_imc").val(imc.toFixed(2))
    });
});