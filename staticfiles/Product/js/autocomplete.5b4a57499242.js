$(function(){
    $("#id_business").autocomplete({
        source:"{% url 'Product:add-general' %}"
    });
});