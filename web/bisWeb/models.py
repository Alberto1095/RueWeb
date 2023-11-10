from django.db import models

# Create your models here.
class Raid(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

class RaidBoss(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.TextField()
    raid = models.ForeignKey(Raid,on_delete=models.CASCADE, blank=True,null=True)    

    def __str__(self):
        return self.raid.name + " - "+self.name

class BossItem(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.TextField(unique=True)
    boss = models.ForeignKey(RaidBoss,on_delete=models.CASCADE, blank=True,null=True) 

    def __str__(self):
        return self.boss.name + " - "+self.name   

class Player(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.TextField(unique=True)
    bisItems = models.ManyToManyField(BossItem)

    def __str__(self):
        return self.name 


