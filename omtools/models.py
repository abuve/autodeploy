from django.db import models

from user_center import models as USER_MODELS


class MongodbMission(models.Model):
    op_type_choices = (
        (1, 'select'),
        (2, 'delete'),
        (3, 'update'),
        (4, 'create'),
    )
    op_type = models.IntegerField(verbose_name=u'操作类型', choices=op_type_choices, default=1)
    title = models.CharField(verbose_name=u'任务标题', max_length=200)
    op_exec = models.CharField(verbose_name=u'执行语句', max_length=2000)
    req_user = models.ForeignKey(USER_MODELS.UserProfile, related_name='mongo_req_user', null=True, blank=True)
    op_user = models.ForeignKey(USER_MODELS.UserProfile, related_name='mongo_op_user', null=True, blank=True)
    status_choices = (
        (1, 'Success'),
        (2, 'Pendding'),
    )
    status = models.IntegerField(verbose_name=u'任务状态', choices=status_choices, default=2)
    date = models.DateTimeField(auto_now_add=True)
    memo = models.CharField(verbose_name='备注', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Mongodb任务表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0},{1},{2}".format(self.op_type, self.title, self.status_choices)

    __str__ = __unicode__