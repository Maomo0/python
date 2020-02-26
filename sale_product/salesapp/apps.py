from django.apps import AppConfig


class SalesappConfig(AppConfig):
    name = 'salesapp'
    verbose_name = '详细情况'  # 需要在__init__文件中加default_app_config = 'salesapp.apps.SalesappConfig'，即可完成修改


