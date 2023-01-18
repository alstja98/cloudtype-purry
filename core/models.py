# Create your models here.
from django.db import models

class Images(models.Model):
    path = models.CharField(max_length=1000)
    update_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    prompt_id= models.ForeignKey('Prompt', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'


class Prompt(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prompt'


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=500)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'