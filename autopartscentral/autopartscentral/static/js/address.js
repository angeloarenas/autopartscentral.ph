/**
 * Created by angeloarenas on 15/01/2017.
 */

var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    $(".address_delete").click(function() {
        var address = $(this).data("address");
        $.post(
            "/account/addresses/delete/",
            {address: address},
            function() {
                location.reload(true);
            });
    });
    $(".address_setdefault").click(function() {
        var address = $(this).data("address");
        $.post(
            "/account/addresses/setdefault/",
            {address: address},
            function() {
                location.reload(true);
            });
    });
});
