function setTime() {
    var select = '<select name="time" class="form-control">';
    for (var hour = 00; hour < 24; hour++) {
        select += '<option>' + hour + ':00 </option>';
        select += '<option>' + hour + ':30 </option>';
    }
    select += '</select>';
    return select;
}
document.getElementById("FromTime").innerHTML = setTime();
document.getElementById("ToTime").innerHTML = setTime();
