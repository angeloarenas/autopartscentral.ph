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
                var options = '<option selected disabled>Model</option>';
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
                var options = '<option selected disabled>Year</option>';
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
});