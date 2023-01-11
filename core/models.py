# Create your models here.
from django.db import models


class Images(models.Model):
    seq = models.ForeignKey('User', models.DO_NOTHING, db_column='seq')
    path = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'images'


class User(models.Model):
    seq = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'user'