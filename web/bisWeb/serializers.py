from rest_framework import serializers
from .models import *


class ItemPickedSerializer(serializers.ModelSerializer):    

    class Meta:
        model = ItemPicked
        fields = ['player','bossItem','itemLevel']

class PlayerSerializer(serializers.ModelSerializer):      

    class Meta:
        model = Player
        fields = ['id', 'name']

class BossItemSerializer(serializers.ModelSerializer):   
    players = PlayerSerializer(many=True, read_only=True)    

    class Meta:
        model = BossItem
        fields = ['id', 'name','players']

class RaidBossSerializer(serializers.ModelSerializer):
    items = BossItemSerializer(many=True, read_only=True)    

    class Meta:
        model = RaidBoss
        fields = ['id', 'name', 'items']