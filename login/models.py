from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.IntegerField()
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'User'