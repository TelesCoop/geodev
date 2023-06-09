# Generated by Django 3.2.13 on 2022-09-29 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('main', '0032_auto_20220831_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='worldzone',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.document'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='source_link',
            field=models.CharField(blank=True, max_length=100, verbose_name='Lien vers la Ressource (URL)'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='source_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Producteur de la ressource'),
        ),
        migrations.AlterField(
            model_name='thematic',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.document'),
        ),
    ]
