/**
 * Created by aaron on 2017/9/11.
 */


function delete_project_data_fn(project_id) {
    $("#delete_data_html_area").html("Confirm remove Application? All the data will be delete!");
    $("#delete_project_app_fn").attr("onclick", "delete_project_app_fn('delete', " + project_id + ")");
    $("#delete_app_modal").modal('show')
}

function update_project_app_fn(update_type, project_id) {

    var project_name = $('input[name="project_name"]').val();
    var business_unit_id = $('input[name="business_unit_id"]').val();

    $.ajax({
        url: '/projects.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'project_id': project_id, 'project_name': project_name, 'business_unit_id': business_unit_id},
        success: function (data, response, status) {
            window.location.href = "/project.html"
        }
    });
}

function delete_project_app_fn(update_type, project_id) {

    $.ajax({
        url: '/projects.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'project_id': project_id},
        success: function (data, response, status) {
            $("#delete_app_modal").modal('hide');
            $('#do_refresh').trigger("click");
        }
    });
}

function load_logsviews_detail_fn(project_id) {
    // 激活头部菜单
    $(".logsviews_nav_control").removeClass('active')
    $("#" + project_id).addClass('active')

    $.ajax({
        url: '/omtools/logs-' + project_id + '.html',
        type: 'get',
        traditional:true,
        success: function (data, response, status) {
            $("#logsviews_detail_html").html(data)
        }
    });
}

function default_logsviews_detail_fn(project_id) {
    load_logsviews_detail_fn(project_id)
}
