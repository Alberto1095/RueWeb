from django.db import models

# Create your models here.

class RaidBoss(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.TextField()    

    def __str__(self):
        return self.name

class BossItem(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.TextField(unique=True)
    boss = models.ForeignKey(RaidBoss,on_delete=models.CASCADE, blank=True,null=True,related_name="items") 

    def __str__(self):
        return self.boss.name + " - "+self.name   

class Player(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.TextField(unique=True)
    bisItems = models.ManyToManyField(BossItem,blank=True,null=True,related_name="players")

    def __str__(self):
        return self.name 


