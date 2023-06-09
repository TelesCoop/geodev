# Generated by Django 3.2.11 on 2022-04-22 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20220422_1016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('zone__name', 'name'), 'verbose_name': 'pays', 'verbose_name_plural': 'pays'},
        ),
        migrations.AddField(
            model_name='resource',
            name='file',
            field=models.FileField(blank=True, help_text="S'il est défini, le lien vers la source est ignoré", null=True, upload_to='', verbose_name='Fichier source'),
        ),
        migrations.AlterField(
            model_name='news',
            name='countries',
            field=models.ManyToManyField(blank=True, help_text="Ce champ n'est pas encore utilisé", to='main.Country', verbose_name='Pays liés'),
        ),
        migrations.AlterField(
            model_name='news',
            name='thematics',
            field=models.ManyToManyField(blank=True, help_text="Ce champ n'est pas encore utilisé", to='main.Thematic', verbose_name='Thématiques liées'),
        ),
        migrations.AlterField(
            model_name='news',
            name='zones',
            field=models.ManyToManyField(blank=True, help_text="Ce champ n'est pas encore utilisé", to='main.WorldZone', verbose_name='Zones du monde liées'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='source_link',
            field=models.CharField(blank=True, max_length=100, verbose_name='Lien vers la source'),
        ),
    ]
