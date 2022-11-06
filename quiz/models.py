from django.db import models

# Create your models here.
class Cafe(models.Model):
    id = models.IntegerField(primary_key=True)
    place_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30, blank=True, null=True)
    x = models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)
    y = models.DecimalField(max_digits=20, decimal_places=16, blank=True, null=True)

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
        
class Signuptest(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'signupTest'

#    def __str__(self):
#        return self.text
#git test