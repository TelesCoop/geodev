# Generated by Django 3.2.11 on 2022-12-19 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_resource_zones'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentpage',
            name='show_in_footer',
            field=models.BooleanField(default=False, help_text='Si un lien vers cette page devra apparaître dans le bas de page', verbose_name='Faire apparaître dans le bas de page'),
        ),
        migrations.AlterField(
            model_name='actualitytype',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='resourcetype',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='thematic',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='slug'),
        ),
    ]
