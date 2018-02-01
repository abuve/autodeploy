/**
 * Created by aaron on 2017/9/11.
 */

var LogsTableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function (app_id) {
        $('#urlmaps_table').bootstrapTable({
            url: '/server/config/urlmaps/json-' + app_id + '.html',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#urlmaps_toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            //height: 300,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [
                {
                    field: 'id',
                    title: 'ID'
                },
                {
                    field: 'url',
                    title: 'Url'
                },
                {
                    field: 'memo',
                    title: 'Memo'
                },
                {
                    field: 'group_id__name',
                    title: 'Group Name',
                },
                {
                    field: 'group_id__app_id__name',
                    title: 'Application',
                },
                {
                    field: 'group_id__app_id__project_id__name',
                    title: 'Project',
                },
                {
                    field: 'name',
                    title: 'Options',
                    width: 240,
                    align: 'center',
                    formatter: button_operateFormatter
                },
            ]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            departmentname: $("#txt_search_departmentname").val(),
            statu: $("#txt_search_statu").val()
        };
        return temp;
    };
    return oTableInit;
};


var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
    };

    return oInit;
};

function button_operateFormatter(value, row, index) {
    return [
        '<div class="btn-group">',
        '<a type="button" class="btn btn-default btn-xs" onclick="detail_urlmaps_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Detail</a>',
        '<a type="button" class="btn btn-default btn-xs" onclick="edit_urlmaps_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit</a>',
        '<a type="button" class="btn btn-default btn-xs" onclick="delete_urlmaps_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete</a>',
        '</div>'
    ].join('');
}

function detail_urlmaps_data_fn(urlmaps_id) {
    $.ajax({
        url: '/server/config/urlmaps/get_urlmaps_detail.html',
        type: 'post',
        traditional:true,
        data: {'urlmaps_id': urlmaps_id},
        success: function (data, response, status) {
            $('#detail_urlmaps_modal').modal('show');
            $('#detail_urlmaps_html').html(data)
        }
    });
}

function create_urlmaps_fn() {
    $("#update_urlmaps_form").trigger("reset");
    $("#update_urlmaps_fn").attr('onclick', 'update_urlmaps_fn("post")')
}

function delete_urlmaps_data_fn(urlmaps_id) {

    $("#delete_urlmaps_html_area").html("Confirm remove UrlMap ID " + urlmaps_id + " ?")
    $("#delete_urlmaps_data_fn").attr("onclick", "do_delete_urlmaps_fn(" + urlmaps_id + ")")
    $("#delete_urlmaps_modal").modal('show')

}

function edit_urlmaps_data_fn(urlmaps_id) {
    $("#update_urlmaps_fn").attr("onclick", "update_urlmaps_fn('put', " + urlmaps_id + ")")

    $.ajax({
        url: '/server/config/urlmaps/update-server-urlmaps.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'urlmaps_id': urlmaps_id},
        success: function (data, response, status) {

            $('input[name="urlmaps_url"]').val(data[0].url);
            $('select[name="urlmaps_group_id"]').val(data[0].group_id_id);
            $('select[name="urlmaps_cloud_id"]').val(data[0].cloud__id);
            $('select[name="urlmaps_forward_id"]').val(data[0].forward__id);
            $('select[name="urlmaps_instance_id"]').val(data[0].docker__id);
            $('textarea[name="urlmaps_memo"]').val(data[0].memo);
            $("#create_url_maps_modal").modal('show')

        }
    });
}

function checkUrl(urlString){
    if(urlString!=""){
        var reg=/(http|ftp|https|ws):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/;
        if(!reg.test(urlString)){
            alert("Error Http Url...");
            return false;
        } else {
            return true;
        }
    } else {
        alert('Please enter url address...');
        return false;
    }
}

function update_urlmaps_fn(update_type, urlmaps_id) {

    var urlmaps_url = $('input[name="urlmaps_url"]').val();
    var urlmaps_group_id = $('select[name="urlmaps_group_id"]').val();
    var urlmaps_cloud_id = $('select[name="urlmaps_cloud_id"]').val();
    var urlmaps_forward_id = $('select[name="urlmaps_forward_id"]').val();
    var urlmaps_instance_id = $('select[name="urlmaps_instance_id"]').val();
    var urlmaps_memo = $('select[name="urlmaps_memo"]').val();

    if (checkUrl(urlmaps_url)) {
        $.ajax({
            url: '/server/config/urlmaps/update-server-urlmaps.html',
            type: update_type,
            dataType: 'json',
            traditional: true,
            data: {
                'urlmaps_id': urlmaps_id,
                'urlmaps_url': urlmaps_url,
                'urlmaps_group_id': urlmaps_group_id,
                'urlmaps_cloud_id': urlmaps_cloud_id,
                'urlmaps_forward_id': urlmaps_forward_id,
                'urlmaps_instance_id': urlmaps_instance_id,
                'urlmaps_memo': urlmaps_memo,
            },
            success: function (data, response, status) {
                $('#urlmaps_table').bootstrapTable('refresh');
                $("#create_url_maps_modal").modal('hide');
                $("#update_urlmaps_form").trigger("reset");
            }
        });
    }
}

function do_delete_urlmaps_fn(urlmaps_id) {
    $.ajax({
        url: '/server/config/urlmaps/update-server-urlmaps.html',
        type: 'delete',
        dataType: 'json',
        traditional:true,
        data: {'urlmaps_id': urlmaps_id},
        success: function (data, response, status) {
            $('#urlmaps_table').bootstrapTable('refresh');
            $("#delete_urlmaps_modal").modal('hide')
        }
    });
}