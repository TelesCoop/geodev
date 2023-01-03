# Generated by Django 3.2.11 on 2023-01-03 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0077_alter_revision_user'),
        ('main', '0037_auto_20221219_0918'),
    ]

    operations = [
        migrations.CreateModel(
            name='StructureSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkedin', models.URLField(blank=True, help_text='URL de votre page LinkedIn', null=True)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'Paramètre de la structure',
            },
        ),
    ]
