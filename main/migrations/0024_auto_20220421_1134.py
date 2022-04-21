# Generated by Django 3.2.11 on 2022-04-21 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20220419_1418'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analyticsscriptsetting',
            options={'verbose_name': 'Script de suivi du traffic'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',), 'verbose_name': 'pays', 'verbose_name_plural': 'pays'},
        ),
        migrations.AlterModelOptions(
            name='worldzone',
            options={'ordering': ('name',), 'verbose_name': 'zone du monde', 'verbose_name_plural': 'zones du monde'},
        ),
        migrations.AddField(
            model_name='worldzone',
            name='latitude',
            field=models.FloatField(default=0, verbose_name='latitude du centre'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worldzone',
            name='longitude',
            field=models.FloatField(default=0, verbose_name='longitude du centre'),
            preserve_default=False,
        ),
    ]