function load_tree_data(server_id, version) {

    $("#select_version_html_area").html(version)
    $("#version_display_html").html("Version：" + version)

    var setting = {
        view: {
            selectedMulti: false
        },
        async: {
            enable: true,
            url:"/server/webconf/nginx/fileTreeJson-56.html?version=2017-12-28-09-11-22",
            autoParam:["id", "name=n", "level=lv"],
            otherParam:{"server_id": server_id, "version": version},
        },
        callback: {
            onClick: zTreeOnClick
        }
    };

    $.fn.zTree.init($("#treeDemo"), setting);

    // 关闭编辑功能按钮
    $("#create_btn").attr("disabled", "true")
    $("#delete_btn").attr("disabled", "true")
    $("#edit_btn").attr("disabled", "true")
    $("#upload_btn").attr("disabled", "true")
    $("#update_btn").attr("disabled", "true")

    // 激活进入编辑按钮
    $("#enter_edit_btn").removeAttr("disabled");

    // 设置当前选择版本&server_id
    $("input[name='select_version_name']").val(version)
    $("input[name='select_server_id']").val(server_id)

}

function zTreeOnClick(event, treeId, treeNode) {
    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()
    if ( ! treeNode.isParent ){
        // 加载文件内容
        $.ajax({
            url: '/server/webconf/nginx/file-data-' + server_id + '.html',
            type: 'get',
            dataType: 'json',
            data: {'version': version, 'select_id': treeNode.id},
            traditional:true,
            success: function (data, response, status) {
                if (data.status) {
                    $("#conf_html_area").html(data.data)
                    hljs.initHighlighting.called = false;
                    hljs.initHighlighting();
                } else {

                }
            }
        });
    }
};

function load_version_info(server_id) {
    $.ajax({
        url: '/server/webconf/nginx/version-json-' + server_id + '.html',
        async: false,
        type: 'get',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
           if (data.status) {
               console.log(data.data)
               version_data = data.data
           } else {
               version_data = null
           }
        }
    });
    return version_data
}

function create_last_version(server_id) {
    $.ajax({
        url: '/server/webconf/nginx/version-json-' + server_id + '.html',
        type: 'post',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
           if (data.status) {
               set_version_info(server_id)
               alert("Nginx初始版本创建成功！")
           }
        }
    });
}

function set_version_info(server_id) {
    var version_data_list = load_version_info(server_id)
    if (version_data_list) {
        version_list_html = ''
        $.each(version_data_list, function( index, value ) {
            version_list_html += '<li><a href="#" onclick=\'load_tree_data(' + server_id + ',"'+value.name+'")\'>' + value.name + '</a></li>'
        });
        $("#version_list_area").html(version_list_html)
    } else {
        $("#version_list_area").html('<li><a href="#" onclick="create_last_version('+ server_id +')">无版本信息，点击创建！</a></li>')
    }
}

function enter_edit_fn() {
    $("#enter_edit_confirm_modal").modal('show')
}

function enter_edit_confirm_fn() {

    // 将当前版本覆盖至last_version
    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()
    if (version != "last_version"){
        $.ajax({
            url: '/server/webconf/nginx/version-json-' + server_id + '.html',
            type: 'put',
            dataType: 'json',
            data: {'version': version},
            traditional:true,
            success: function (data, response, status) {
                if (data.status) {
                    load_tree_data(server_id, 'last_version')
                }
            }
        });
    }

    // 激活编辑功能按钮
    $("#create_btn").removeAttr("disabled");
    $("#delete_btn").removeAttr("disabled");
    $("#edit_btn").removeAttr("disabled");
    $("#upload_btn").removeAttr("disabled");
    $("#update_btn").removeAttr("disabled");

    // 关闭进入编辑功能
    $("#enter_edit_btn").attr("disabled", "true")

    $("#enter_edit_confirm_modal").modal('hide')

}

function get_current_tree_path(file_tag) {
    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.getSelectedNodes();
    var dir_path_list = []

    dir_path_str = '/'

    if (nodes.length != 0) {
        var node = nodes[0]
        for(i=0; i<=nodes[0].level; i++) {
            node = node.getParentNode()
            if (! node) {
                break
            }
            dir_path_list.unshift(node.name)
        }

        for (index in dir_path_list) {
            dir_path_str += dir_path_list[index] + '/'
        }

        if (file_tag) {
            dir_path_str += nodes[0].name
        } else {
            if (nodes[0].isParent) {
                dir_path_str += nodes[0].name + '/'
            }
        }

    }

    return dir_path_str
}

function create_fn() {
    var dir_path = get_current_tree_path(file_tag=false)
    $("input[name='create_object_path']").val(dir_path)
    $("#create_modal").modal('show')
}

function do_create() {
    var create_object_name = $("input[name='create_object_name']").val()
    var create_object_path = $("input[name='create_object_path']").val()
    var create_object_type = $("input[name='create_object_type']:checked").val()

    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()

    if (create_object_name.length == 0) {
        alert("Please enter file name.")
        return false
    }

    $.ajax({
        url: '/server/webconf/nginx/file-data-' + server_id + '.html',
        type: 'post',
        dataType: 'json',
        data: {'version': version, 'create_object_name': create_object_name, 'create_object_path': create_object_path, 'create_object_type': create_object_type},
        traditional:true,
        success: function (data, response, status) {
            if (data.status) {
                console.log(data)
            } else {

            }
        }
    });
}