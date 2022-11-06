from django.db import models

# Create your models here.
class Cafe(models.Model):
    id = models.IntegerField(primary_key=True)
    cafe_name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'Cafe'


class Review(models.Model):
    reviewer_name = models.CharField(primary_key=True, max_length=64)
    content = models.CharField(max_length=512)
    id = models.ForeignKey(Cafe, models.DO_NOTHING, db_column='id')

    class Meta:
        managed = False
        db_table = 'Review'
        unique_together = (('reviewer_name', 'content', 'id'),)
        
        
#git test