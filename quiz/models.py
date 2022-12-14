from django.db import models



# Create your models here.
class Cafe(models.Model):
    id = models.IntegerField(primary_key=True)
    place_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30, blank=True, null=True)
    x = models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)
    y = models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)
    road_address_name = models.CharField(max_length=128, blank=True, null=True)
    main_photo = models.CharField(max_length=128, blank=True, null=True)
    star_mean = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    bookmark_cnt = models.IntegerField()
    comment_count = models.IntegerField(blank=True, null=True)
    effective = models.IntegerField(blank=True, null=True)
    clean = models.IntegerField(blank=True, null=True)
    tasty = models.IntegerField(blank=True, null=True)
    vibe = models.IntegerField(blank=True, null=True)
    kind = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Cafe'

class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Cafe, models.DO_NOTHING)
    username = models.CharField(max_length=100, blank=True, null=True)
    contents = models.CharField(max_length=512, blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    photocnt = models.IntegerField(db_column='photoCnt', blank=True, null=True)  # Field name made lowercase.
    likecnt = models.IntegerField(db_column='likeCnt', blank=True, null=True)  # Field name made lowercase.
    usercommentcount = models.IntegerField(db_column='userCommentCount', blank=True, null=True)  # Field name made lowercase.
    usercommentaveragescore = models.DecimalField(db_column='userCommentAverageScore', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(max_length=20, blank=True, null=True)
    kakaomapuserid = models.CharField(db_column='kakaoMapUserId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    photolist = models.CharField(db_column='photoList', max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Review'
        unique_together = (('id', 'store'),)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'User'

class Bookmark(models.Model):
    user_id = models.IntegerField(primary_key=True)
    id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Bookmark'
        unique_together = (('user_id', 'id'),)


        