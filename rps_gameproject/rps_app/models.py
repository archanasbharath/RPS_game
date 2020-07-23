from django.db import models

class Score(models.Model):
    Player_score= models.IntegerField(default=0)
    System_score= models.IntegerField(default=0)


class User(models.Model):
    User_Name= models.CharField(max_length=100)
    Mail_id= models.CharField(max_length=100)
    password=models.CharField(max_length=15)

