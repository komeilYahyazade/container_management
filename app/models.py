from django.db import models
import docker


class App(models.Model):
    name = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
    envs = models.JSONField()
    command = models.CharField(max_length=256)


class Container(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    container_id = models.CharField(max_length=256, default="running")
    name = models.CharField(max_length=256, default='')
    image = models.CharField(max_length=256, default="")
    envs = models.JSONField(blank=True, null=True)
    command = models.CharField(max_length=256, default="")
    app = models.ForeignKey(App, related_name='containers',
                            on_delete=models.DO_NOTHING)
