from django.db import models

from cmdb import models as CMDB_MODELS

class ProjectInfo(models.Model):
    """
    项目信息表
    """
    name = models.CharField(max_length=64, unique=True)
    #project_path = models.CharField('系统目录', max_length=200, unique=True)
    business_unit = models.ForeignKey(CMDB_MODELS.BusinessUnit, verbose_name='归属业务线', null=True, blank=True,
                                      on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "项目信息表"

    def __str__(self):
        return self.name


class Applications(models.Model):
    """
    应用信息表
    """
    name = models.CharField(max_length=64, unique=True)
    app_type_choices = (
        ('java', 'java'),
        ('php', 'php'),
        ('python', 'python'),
        ('worker', 'worker'),
        ('static', 'static'),
        ('nodejs', 'nodejs'),
    )
    app_type = models.CharField(choices=app_type_choices, max_length=10, default='java')
    project_id = models.ForeignKey(ProjectInfo, related_name='applications')
    leader = models.CharField('开发leader', max_length=40, blank=True, null=True)
    members = models.CharField('开发成员', max_length=40, blank=True, null=True)
    #group = models.ManyToManyField(AppGroups, related_name='groups')

    class Meta:
        verbose_name_plural = "应用信息表"

    def __str__(self):
        return self.name


class AppGroups(models.Model):
    """
    应用分组表
    """
    name = models.CharField('分组名称', max_length=64)
    #config_path = models.CharField('应用路径', max_length=200, blank=True, null=True)
    yaml_path = models.CharField('YAML配置文件路径', max_length=200, blank=True, null=True)
    app_id = models.ForeignKey(Applications, related_name='groups')
    instance = models.ManyToManyField(CMDB_MODELS.DockerInstance, related_name='instances')

    class Meta:
        unique_together = ('name', 'app_id',)
        verbose_name_plural = "应用分组表"

    def __str__(self):
        return self.name


class AppInstances(models.Model):
    """
    应用实例表
    """
    ip = models.GenericIPAddressField('IP地址', blank=True, null=True)
    port = models.SmallIntegerField('实例端口', blank=True, null=True)
    group_id = models.ForeignKey(AppGroups, related_name='instances')
    asset_number = models.CharField('资产编号(CMDB)', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = "应用实例表"

    def __str__(self):
        return self.ip


class DockerYamlConf(models.Model):
    """
    Docker yaml 配置管理
    """
    group_id = models.OneToOneField("AppGroups")
    yaml_data = models.TextField()
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "YAML配置表"

    def __str__(self):
        return str(self.group_id)


class WebConfig(models.Model):
    """
    转发服务配置表
    """
    config_type_choices = (
        (1, 'Nginx'),
        (2, 'Forward'),
        (3, 'HA'),
    )
    config_type_id = models.IntegerField(choices=config_type_choices, default=1)
    business_unit = models.ForeignKey(CMDB_MODELS.BusinessUnit, verbose_name='归属业务线', null=True, blank=True,
                                      on_delete=models.SET_NULL)
    # memo = models.CharField('备注', max_length=64, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "转发服务配置表"

    def __str__(self):
        return self.get_config_type_id_display()


class MissionAppInstance(models.Model):
    """
    任务-应用实例表
    """
    ip = models.GenericIPAddressField('IP地址', blank=True, null=True)
    status = models.SmallIntegerField('任务状态', default=0)

    class Meta:
        verbose_name_plural = "任务-应用实例表"

    def __str__(self):
        return self.ip


class MissionApp(models.Model):
    """
    任务-应用信息表
    """
    name = models.CharField(max_length=64)
    ip = models.ManyToManyField(MissionAppInstance, related_name='mission_apps')
    status = models.SmallIntegerField('任务状态', default=0)

    class Meta:
        verbose_name_plural = "任务-应用信息表"

    def __str__(self):
        return self.name


class MissionProject(models.Model):
    """
    任务-项目信息表
    """
    name = models.CharField(max_length=64)
    app = models.ManyToManyField(MissionApp, related_name='mission_projects')

    class Meta:
        verbose_name_plural = "任务-项目信息表"

    def __str__(self):
        return self.name


class Mission(models.Model):
    """
    任务管理表
    """
    name = models.CharField(max_length=64)
    mission_type_choices = (
        (1, 'Update'),
        (2, 'Restart'),
        (3, 'Rollback'),
        (4, 'Stop'),
    )
    mission_type = models.SmallIntegerField(choices=mission_type_choices, default=1)
    project = models.ManyToManyField(MissionProject, related_name='missions')

    class Meta:
        verbose_name_plural = "任务管理表"

    def __str__(self):
        return self.name