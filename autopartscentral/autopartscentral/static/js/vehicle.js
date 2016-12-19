/**
 * Created by angeloarenas on 18/12/2016.
 */

var response_cache_models = {};
function fill_vehicle_models(make_id) {
    if (response_cache_models[make_id]) {
        $("#filter_vehicle_model").html(response_cache_models[make_id]);
    } else {
        $.getJSON(
            "/ajax/",
            {vehicle_make: make_id},
            function(ret) {
                var options = '<option value=0 selected disabled>Model</option>';
                for (var i in ret)
                    options += '<option value="' + ret[i].id + '">' + ret[i].name + '</option>';
                response_cache_models[make_id] = options;
                $("#filter_vehicle_model").html(options);
            });
    }
}

var response_cache_years = {};
function fill_vehicle_years(model_id) {
    if (response_cache_years[model_id]) {
        $("#filter_vehicle_year").html(response_cache_years[model_id]);
    } else {
        $.getJSON(
            "/ajax/",
            {vehicle_model: model_id},
            function(ret) {
                var options = '<option value=0 selected disabled>Year</option>';
                for (var i in ret)
                    options += '<option value="' + ret[i].id + '">' + ret[i].name + '</option>';
                response_cache_years[model_id] = options;
                $("#filter_vehicle_year").html(options);
            });
    }
}

$(document).ready(function() {
    $("#filter_vehicle_make").change(function() { fill_vehicle_models($(this).val()); });
    $("#filter_vehicle_model").change(function() { fill_vehicle_years($(this).val()); });

    $("#set_vehicle_filter").click(function () {
        var uri = new URI();
        uri.setSearch("make", $("#filter_vehicle_make").val());
        uri.setSearch("model", $("#filter_vehicle_model").val());
        uri.setSearch("year", $("#filter_vehicle_year").val());
        window.location = uri;
    });
    $("#clear_vehicle_filter").click(function () {
        var uri = new URI();
        uri.removeSearch(["make", "model", "year"]);
        window.location = uri;
    });

    $('.set_category_1_filter').click(function () {
        var uri = new URI();
        uri.setSearch("category1", $(this).data("name"));
        uri.removeSearch(["category2", "category3"]);
        window.location = uri;
    });
    $('.set_category_2_filter').click(function () {
        var uri = new URI();
        uri.setSearch("category2", $(this).data("name"));
        uri.removeSearch(["category1", "category3"]);
        window.location = uri;
    });
});
