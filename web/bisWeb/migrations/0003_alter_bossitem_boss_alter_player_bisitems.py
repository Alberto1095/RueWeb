# Generated by Django 4.2.7 on 2023-11-10 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bisWeb', '0002_raidboss_raid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bossitem',
            name='boss',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='bisWeb.raidboss'),
        ),
        migrations.AlterField(
            model_name='player',
            name='bisItems',
            field=models.ManyToManyField(blank=True, null=True, related_name='players', to='bisWeb.bossitem'),
        ),
    ]
