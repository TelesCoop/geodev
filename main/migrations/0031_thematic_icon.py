# Generated by Django 3.2.13 on 2022-08-31 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('main', '0030_auto_20220831_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='thematic',
            name='icon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.document'),
        ),
    ]