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
            function(data) {
                //TODO Update cart
                $('#cart_updated_modal').modal('toggle').find('div.modal-body').text(data);
            })
            .error(function(data) {
                $('#cart_updated_modal').modal('toggle').find('div.modal-body').text(data.responseText);
        });
    });
    $(".cart_remove").click(function() {
        var part_slug = $(this).data("slug");
        $.post(
            "/cart/remove/",
            {part: part_slug},
            function() {
                location.reload(true);
            });
    });
    //TODO Use id instead of slug
    $("#cart_update").click(function() {
        var data = [];
        $(".cart_item_row").each(function() {
            var quantity = $(this).find('.cart_item_quantity').val();
            if(quantity) {
                data.push(
                    {
                        part: $(this).find('.cart_remove').data("slug"),
                        quantity: quantity
                    }
                );
            }
        });
        $.post(
            "/cart/update/",
            {data: JSON.stringify(data)},
            function() {
                location.reload(true);
            });
    });
});
