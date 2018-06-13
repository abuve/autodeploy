/**
 * Created by aaron on 2017/9/11.
 */

var OmToolsLogsInit = function () {
    var oTableInit = new Object();
    // 初始化Table
    oTableInit.Init = function (project_id) {
        $('#omtools_logs_table').bootstrapTable({
            url: '/omtools/logs-' + project_id + '.html',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#omtools_logs_toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 40,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: false,
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
                    field: 'project_id__name',
                    title: '项目名称'
                },
                {
                    field: 'server_node',
                    title: '节点名称'
                },
                {
                    field: 'server_type',
                    title: '环境类型',
                    formatter: server_type_formatter
                },
                {
                    field: 'logs_type',
                    title: '日志地址',
                    formatter: logs_type_formatter
                },
                {
                    field: 'memo',
                    title: '备注信息'
                },
            ]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   // 这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            departmentname: $("#txt_search_departmentname").val(),
            statu: $("#txt_search_statu").val()
        };
        return temp;
    };
    return oTableInit;
};

function logs_type_formatter(value, row, index) {
    return '<a href="' + row.url + '" target="_blank">' + row.logs_type + '</a>'
}

function server_type_formatter(value, row, index) {
    var type_map = {0: '客服测试', 1: '正式环境', 2: '开发环境'}
    return type_map[row.server_type]
}

function delete_project_data_fn(project_id) {
    $("#delete_data_html_area").html("Confirm remove Application? All the data will be delete!");
    $("#delete_project_app_fn").attr("onclick", "delete_project_app_fn('delete', " + project_id + ")");
    $("#delete_app_modal").modal('show')
}


function load_logsviews_detail_fn(project_id) {
    // 激活头部菜单
    $(".logsviews_nav_control").removeClass('active')
    $("#" + project_id).addClass('active')

    opt = {
        url: '/omtools/logs-' + project_id + '.html'
    }

    $("#omtools_logs_table").bootstrapTable('refresh', opt)
}

function default_logsviews_detail_fn(project_id) {

    // 激活头部菜单
    $(".logsviews_nav_control").removeClass('active')
    $("#" + project_id).addClass('active')

    var omtoolsLogs = new OmToolsLogsInit();
    omtoolsLogs.Init(project_id);
}
