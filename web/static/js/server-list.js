/**
 * Created by aaron on 2017/9/11.
 */

function update_server_group_fn(update_type, group_id) {

    var add_group_name = $('input[name="add_group_name"]').val()
    var add_group_app_id = $('input[name="add_group_app_id"]').val()
    var add_group_app_path = $('input[name="add_group_app_path"]').val()

    $.ajax({
        url: '/update-server-group.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'add_group_name': add_group_name, 'add_group_app_id': add_group_app_id, 'add_group_app_path': add_group_app_path, 'group_id': group_id},
        success: function (data, response, status) {
            $('#group_table').bootstrapTable('refresh');
            $("#add_group_modal").modal('hide')
            $("#delete_group_modal").modal('hide')
            $("#add_server_group_form").trigger("reset");
        }
    });
}