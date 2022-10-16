from django.db import models

# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    answer = models.IntegerField()
    
class Cafe(models.Model):
    name = models.CharField(max_length=100)
    charactor = models.CharField(max_length = 100)
    grade = models.IntegerField()
    Location = models.CharField(max_length = 100)
    
    