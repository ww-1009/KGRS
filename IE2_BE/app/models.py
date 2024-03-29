from django.db import models


# Create your models here.
class FdClassForest(models.Model):
    class_name = models.CharField(max_length=255, blank=True, null=True)
    sup = models.CharField(max_length=255, blank=True, null=True)
    sub = models.TextField(blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fd_class_forest'


class FdEntity(models.Model):
    id = models.IntegerField(primary_key=True)
    entity = models.CharField(max_length=100)
    imgurl = models.CharField(db_column='imgUrl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    relatedtype = models.TextField(db_column='relatedType', blank=True, null=True)  # Field name made lowercase.
    abstract = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fd_entity'


class FdRelation(models.Model):
    id_s = models.IntegerField(db_column='id_S', primary_key=True)  # Field name made lowercase.
    s = models.CharField(db_column='S', max_length=100)  # Field name made lowercase.
    p = models.CharField(db_column='P', max_length=100)  # Field name made lowercase.
    o = models.CharField(db_column='O', max_length=100)  # Field name made lowercase.
    id_o = models.IntegerField(db_column='id_O')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fd_relation'
        unique_together = (('id_s', 'id_o'),)

class FdTop5(models.Model):
    id = models.IntegerField(primary_key=True)
    top1_id = models.IntegerField(blank=True, null=True)
    value1 = models.FloatField(blank=True, null=True)
    top2_id = models.IntegerField(blank=True, null=True)
    value2 = models.FloatField(blank=True, null=True)
    top3_id = models.IntegerField(blank=True, null=True)
    value3 = models.FloatField(blank=True, null=True)
    top4_id = models.IntegerField(blank=True, null=True)
    value4 = models.FloatField(blank=True, null=True)
    top5_id = models.IntegerField(blank=True, null=True)
    value5 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fd_top5'

class SelfEntity(models.Model):
    entity = models.CharField(max_length=255, blank=True, null=True)
    imgurl = models.CharField(db_column='imgUrl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    relatedtype = models.CharField(db_column='relatedType', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    abstract = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    user_id = models.IntegerField()
    graph_id = models.IntegerField()
    entity_id = models.IntegerField()
    deleted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'self_entity'


class SelfRelation(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    graph_id = models.IntegerField()
    relation_id = models.IntegerField()
    id_s = models.IntegerField(db_column='id_S', blank=True, null=True)  # Field name made lowercase.
    s = models.CharField(db_column='S', max_length=255, blank=True, null=True)  # Field name made lowercase.
    p = models.CharField(db_column='P', max_length=255, blank=True, null=True)  # Field name made lowercase.
    o = models.CharField(db_column='O', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_o = models.IntegerField(db_column='id_O', blank=True, null=True)  # Field name made lowercase.
    update_time = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'self_relation'


class SelfGraphInfo(models.Model):
    user_id = models.IntegerField()
    graph_id = models.IntegerField()
    graph_name = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'self_graph_info'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
