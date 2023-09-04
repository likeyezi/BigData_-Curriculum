# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class InputToClean(models.Model):
    id = models.IntegerField(primary_key=True)
    cname = models.CharField(max_length=50, blank=True, null=True)
    mname = models.CharField(max_length=50, blank=True, null=True)
    sname = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    svolume = models.FloatField(blank=True, null=True)
    mount = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'input_to_clean'


class Output(models.Model):
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    baby = models.IntegerField(blank=True, null=True)
    menstruation = models.IntegerField(blank=True, null=True)
    loyalty = models.CharField(max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    identity = models.CharField(max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    tendency = models.CharField(max_length=255, db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'output'
