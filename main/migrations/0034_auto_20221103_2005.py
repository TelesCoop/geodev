# Generated by Django 3.2.13 on 2022-11-03 19:05

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20220929_1836'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resource',
            options={'ordering': ('name',), 'verbose_name': 'Ressource', 'verbose_name_plural': 'Ressources'},
        ),
        migrations.AddField(
            model_name='profile',
            name='types',
            field=models.ManyToManyField(to='main.ResourceType', verbose_name='types de ressource'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='short_description',
            field=wagtail.fields.RichTextField(blank=True, max_length=1000, null=True, verbose_name='Description courte'),
        ),
    ]
