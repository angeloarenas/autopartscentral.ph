/**
 * Created by angeloarenas on 22/12/2016.
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
    $("#cart_add").click(function() {
        var part_slug = $(this).data("slug");
        $.post(
            "/cart/add/",
            {part: part_slug},
            function(ret, status) {
                console.log(status);
                //update cart html, success modal
            });
    });
});
