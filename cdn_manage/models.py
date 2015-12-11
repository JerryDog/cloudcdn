from django.db import models
import datetime
# Create your models here.

class Domain(models.Model):
    domain_name = models.CharField(max_length=64)
    domain_type = models.CharField(max_length=20)
    domain_status = models.CharField(max_length=20)
    domain_id = models.CharField(max_length=64)
    ip_list = models.CharField(max_length=128)
    project_id = models.CharField(max_length=64)
    user_name = models.CharField(max_length=32)
    test_url = models.URLField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

class CacheRules(models.Model):
    cache_path = models.CharField(max_length=64)
    cache_time = models.CharField(max_length=64)
    ignore_param_req = models.BooleanField()
    domain_table_id = models.IntegerField()

class TaskList(models.Model):
    task_id = models.CharField(max_length=64)
    project_id = models.CharField(max_length=64)
    task_type = models.CharField(max_length=32)
    task_content = models.CharField(max_length=1024)
    task_status = models.CharField(max_length=18)
    task_user = models.CharField(max_length=32)
    task_create_at = models.DateTimeField(auto_now_add=True)
    task_done_at = models.DateTimeField(auto_now_add=True)


class AccessControl(models.Model):
    url_type = models.CharField(max_length=64)
    white_list = models.CharField(max_length=128)
    black_list = models.CharField(max_length=128)
    deny_list = models.CharField(max_length=128)
    domain_id = models.IntegerField()


class DailyBandwidth(models.Model):
    domain_name = models.CharField(max_length=64)
    project_id = models.CharField(max_length=64)
    bandwidth = models.CharField(max_length=64)
    date = models.DateTimeField()
    update_at = models.DateTimeField(auto_now_add=True)
