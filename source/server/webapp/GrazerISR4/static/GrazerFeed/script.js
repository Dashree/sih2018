function setTime(NAME) {
    var select = '<select name="' + NAME + '" class="form-control" required>';
    for (var hour = 00; hour < 24; hour++) {
        select += '<option>' + hour + ':00 </option>';
        select += '<option>' + hour + ':30 </option>';
    }
    select += '</select>';
    return select;
}
document.getElementById("FromTime").innerHTML = setTime('{{ form.FromTime.name }}');
document.getElementById("ToTime").innerHTML = setTime('{{ form.ToTime.name }}');

function hide() {
    var x = document.getElementById("video");
    if (x.style.display == 'none') {
        x.style.display = 'block';
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken')