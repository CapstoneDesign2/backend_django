from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'User'