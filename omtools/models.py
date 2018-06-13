from django.db import models

from user_center import models as USER_MODELS
from repository import models as REPOSITORY_MODELS
from cmdb import models as CMDB_MODELS


class MongodbMission(models.Model):
    op_type_choices = (
        (1, 'find'),
        (2, 'delete'),
        (3, 'update'),
        (4, 'create'),
    )
    op_type = models.IntegerField(verbose_name=u'操作类型', choices=op_type_choices, default=1)
    title = models.CharField(verbose_name=u'任务标题', max_length=200)
    op_exec = models.CharField(verbose_name=u'执行语句', max_length=2000)
    database = models.CharField(verbose_name=u'执行数据库', max_length=100)
    document = models.CharField(verbose_name=u'执行表', max_length=100)
    find = models.CharField(verbose_name=u'find查询', max_length=2000)
    update = models.CharField(verbose_name=u'update更新', max_length=2000, null=True, blank=True)
    multi_tag = models.BooleanField(u'批量更新', default=False)
    req_user = models.ForeignKey(USER_MODELS.UserProfile, related_name='mongo_req_user', null=True, blank=True)
    op_user = models.ForeignKey(USER_MODELS.UserProfile, related_name='mongo_op_user', null=True, blank=True)
    approval_md5 = models.CharField(verbose_name=u'md5审核值', max_length=100)
    approved = models.BooleanField(u'批准执行', default=False)
    status_choices = (
        (1, 'Success'),
        (2, 'Pendding'),
        (3, 'Warning'),
    )
    status = models.IntegerField(verbose_name=u'任务状态', choices=status_choices, default=2)
    op_detail = models.CharField(verbose_name='执行详情', max_length=200, null=True, blank=True, default='等待执行')
    date = models.DateTimeField(auto_now_add=True)
    memo = models.CharField(verbose_name='备注', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Mongodb任务表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0},{1},{2}".format(self.op_type, self.title, self.status_choices)

    __str__ = __unicode__


class MongodbMissionTemplate(models.Model):
    op_type_choices = (
        (1, 'find'),
        (2, 'delete'),
        (3, 'update'),
        (4, 'create'),
    )
    op_type = models.IntegerField(verbose_name=u'操作类型', choices=op_type_choices, default=1)
    title = models.CharField(verbose_name=u'任务标题', max_length=200)
    database = models.CharField(verbose_name=u'执行数据库', max_length=100)
    document = models.CharField(verbose_name=u'执行表', max_length=100)
    find = models.CharField(verbose_name=u'find查询', max_length=100)
    update = models.CharField(verbose_name=u'update更新', max_length=100, null=True, blank=True)
    var_dict = models.CharField(verbose_name=u'变量字典', max_length=2000)
    op_exec = models.CharField(verbose_name=u'模板语句', max_length=2000)
    multi_tag = models.BooleanField(u'批量更新',default=False)
    approve_mail = models.CharField(u'审批人邮箱', max_length=100, null=True, blank=True)
    note = models.TextField(verbose_name=u'提示信息', null=True, blank=True)
    memo = models.CharField(verbose_name='备注', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Mongodb任务模板表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0},{1}".format(self.op_type, self.title)

    __str__ = __unicode__


class LogsControl(models.Model):
    project_id = models.ForeignKey(REPOSITORY_MODELS.ProjectInfo, related_name='logscontrol')
    # server_obj = models.ForeignKey(CMDB_MODELS.Asset, related_name='logsserver')
    server_node = models.CharField(u'节点名称', max_length=100)
    server_type_choices = (
        (0, '客服测试'),
        (1, '正式环境'),
        (2, '开发环境'),
    )
    server_type = models.SmallIntegerField(choices=server_type_choices, default=1)
    # logs_type_choices = (
    #     (0, '错误日志'),
    #     (1, '默认日志'),
    # )
    logs_type = models.CharField('日志类型', max_length=100)
    url = models.URLField('日志地址', blank=True, null=True)
    memo = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "项目日志表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}\t{1}".format(self.project_id.name, self.server_node, self.url)

    __str__ = __unicode__