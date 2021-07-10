from django.db import models


class Raw(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    post_text = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=128, blank=True, null=True)
    author_profile = models.CharField(max_length=255, blank=True, null=True)
    post_time = models.DateTimeField(blank=True, null=True)
    extract_time = models.DateTimeField(blank=True, null=True)
    post_link = models.CharField(max_length=255, blank=True, null=True)
    post_group = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'raw'


class Structured(models.Model):
    id = models.OneToOneField(Raw, models.DO_NOTHING, db_column='id', primary_key=True)
    loc_from = models.CharField(max_length=255, blank=True, null=True)
    loc_to = models.CharField(max_length=255, blank=True, null=True)
    n_seats = models.CharField(max_length=16, blank=True, null=True)
    cov_day = models.CharField(max_length=64, blank=True, null=True)
    cov_time = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    cost = models.CharField(max_length=16, blank=True, null=True)
    categ = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structured'


class Test(models.Model):
    col1 = models.IntegerField(blank=True, null=True)
    col2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'
