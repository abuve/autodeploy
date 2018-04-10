/**
 * Created by aaron on 2017/9/11.
 */

// 加载模板详情数据
function load_template_component_fn(value) {

    var selectedOption = value.options[value.selectedIndex];

    if (selectedOption.value != 'None') {
        var template_id = selectedOption.value

        $.ajax({
            url: '/omtools/mongodb-get-template.html',
            type: 'get',
            dataType: 'json',
            traditional:true,
            data: {'template_id': template_id},
            success: function (data, response, status) {
                if (data) {
                    var var_list = JSON.parse(data.data.var_dict)
                    var $body = $('#mongo_mission_var_detail');
                    $body.empty()

                    // 显示模板语句
                    var tr = document.createElement('tr');
                    var td = document.createElement('td');
                    td.innerHTML = 'Option Template :'
                    td.setAttribute('style', 'line-height: 34px; width: 180px;')
                    td.setAttribute('align', 'right')
                    $(tr).append(td);

                    var td = document.createElement('td');
                    td.innerHTML = '<p class="bg-info" style="padding: 10px; font-weight: bold" >' + data.data.op_exec + '</p>'
                    td.setAttribute('colspan', '2')
                    $(tr).append(td);

                    $body.append(tr);

                    $.each(var_list, function (index) {
                        var tr = document.createElement('tr');

                        // 定义变量name
                        var td = document.createElement('td');
                        td.innerHTML = '自定义变量 ' + var_list[index].var_name
                        td.setAttribute('align', 'right')
                        td.setAttribute('style', 'width: 180px;')
                        $(tr).append(td);

                        // 自定义变量值
                        var td = document.createElement('td');
                        if (var_list[index].type == 'textarea') {
                            td.innerHTML = '<textarea type="textarea" class="form-control" rows="5" id="mongoMission_var_1" name="' + var_list[index].var_name + '" placeholder="输入提案id，每行一个"></textarea>'
                        }
                        if (var_list[index].type == 'select') {
                            var select_option_html = ""
                            for(var value_index in var_list[index].select){
                                select_option_html += '<option value="' + var_list[index].select[value_index] + '">' + var_list[index].select[value_index] + '</option>'
                            }
                            td.innerHTML = '<select class="form-control" name="' + var_list[index].var_name + '" id="select' + index + '">' + select_option_html + '</select>'
                        }

                        $(tr).append(td);

                        // 变量值类型
                        var td = document.createElement('td');
                        td.innerHTML = '<a type="button" class="btn btn-info btn-xs">' + var_list[index].choice + '</a>'
                        td.setAttribute('style', 'line-height: 34px;')
                        $(tr).append(td);

                        $body.append(tr);

                    });

                }
            }
        });

        // 显示提交按钮
        $("#create_mongodbMission_btn").show()

        // 显示任务备注
        $("#mongoMission_memo").show()

    }
}

function create_mongodbMission_fn() {
    $("#mongoMission_add_modal").modal({show: true, backdrop: 'static', keyboard: false})
}

function do_create_mongodbMission() {
    // 表单数据校验
    var template_id = $("select[name='mongoMission_template_id']").val()
    if (template_id == 'None') {
        alert('请选择任务模板！')
        return false;
    }

    // 控制显示
    $('#mission_create_loading').show()
    $('#create_mongodbMission_cancel_btn').hide()
    $('#create_mongodbMission_btn').hide()


    $.ajax({
        url: '/omtools/mongodb-json.html',
        type: 'post',
        dataType: 'json',
        traditional:true,
        data: $('#add_mongoMission_form').serialize(),
        success: function (data, response, status) {
            if (data.status) {
                $("#mongoMission_add_modal").modal('hide')
                document.getElementById("add_mongoMission_form").reset()
                $('#do_refresh').trigger("click");

                // 控制显示
                $('#mission_create_loading').hide()
                $('#create_mongodbMission_cancel_btn').show()
                $('#create_mongodbMission_btn').show()
            }
        }
    });

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

function show_mission_opdetail_fn(id) {
    $.ajax({
        url: '/omtools/mongodb-get-detail.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'id': id},
        success: function (data, response, status) {
            if (data.status) {
                $("#mission_exec_opdetail_modal").modal('show')
                $("#mission_exec_opdetail_html").html(data.data.op_detail)
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
