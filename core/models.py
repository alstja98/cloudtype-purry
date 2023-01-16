# Create your models here.
from django.db import models


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', models.DO_NOTHING, db_column='id')
    path = models.CharField(max_length=1000)
    update_time = models.DateTimeField(auto_now=True)


    class Meta:
        managed = False
        db_table = 'images'


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=500)
    update_time = models.DateTimeField(auto_now=True)


    class Meta:
        managed = False
        db_table = 'user'