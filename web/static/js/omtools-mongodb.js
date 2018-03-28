/**
 * Created by aaron on 2017/9/11.
 */

function create_mongodbMission_fn() {
    $("#mongoMission_add_modal").modal('show')
}

function do_create_mongodbMission() {
    // 表单数据校验

    // 提交表单
    $("#add_mongoMission_form").submit()
}

function show_mission_detail_fn(id) {
    $.ajax({
        url: '/omtools/mongodb-get-detail.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'id': id},
        success: function (data, response, status) {
            if (data.status) {
                $("#mission_exec_detail_modal").modal('show')
                $("#mission_exec_detail_html").html(data.data.op_exec)
            }
        }
    });
}

function submit_mission_fn(id) {
    $("#do_submit_mongodbMission").attr("onclick", "do_submit_mission(" + id + ")")
    $("#mission_submit_modal").modal('show')
}

function do_submit_mission(id) {
    $.ajax({
        url: '/omtools/mongodb-json.html',
        type: 'put',
        dataType: 'json',
        traditional:true,
        data: {'id': id},
        success: function (data, response, status) {
            if (data.status) {
                $('#do_refresh').trigger("click");
                $("#mission_submit_modal").modal('hide')
            }
        }
    });
}
