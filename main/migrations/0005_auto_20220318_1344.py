# Generated by Django 3.2.11 on 2022-03-18 13:44

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0066_collection_management_permissions"),
        ("wagtailimages", "0023_add_choose_permissions"),
        ("main", "0004_auto_20220318_1117"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="homepage",
            options={"verbose_name": "Page d'accueil"},
        ),
        migrations.AlterModelOptions(
            name="newslistpage",
            options={"verbose_name": "Page des actualités"},
        ),
        migrations.AlterModelOptions(
            name="ressourcespage",
            options={"verbose_name": "Page des ressources"},
        ),
        migrations.AddField(
            model_name="homepage",
            name="introduction",
            field=wagtail.core.fields.RichTextField(
                blank=True,
                null=True,
                verbose_name="Introduction du block des ressources",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="news_block_title",
            field=models.CharField(
                blank=True,
                default="Dernières actualités",
                max_length=64,
                verbose_name="Titre du block des actualités",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="ressources_block_explication",
            field=wagtail.core.fields.RichTextField(
                blank=True,
                help_text="Explication présente sous les listes des différents profils",
                null=True,
                verbose_name="Explication du block des ressources",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="ressources_block_introduction",
            field=wagtail.core.fields.RichTextField(
                blank=True,
                null=True,
                verbose_name="Introduction du block des ressources",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="ressources_block_title",
            field=models.CharField(
                blank=True,
                default="Des ressources adaptées à votre profil",
                max_length=64,
                verbose_name="Titre du block des ressources",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="description",
            field=wagtail.core.fields.RichTextField(
                blank=True, null=True, verbose_name="Description"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="icon",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="profiles",
                to="wagtailimages.image",
            ),
        ),
        migrations.AddField(
            model_name="ressource",
            name="geo_dev_creation",
            field=models.BooleanField(default=False, verbose_name="Créé par GeoDEV ?"),
        ),
        migrations.AddField(
            model_name="ressource",
            name="profiles",
            field=models.ManyToManyField(
                blank=True,
                related_name="ressources",
                to="main.Profile",
                verbose_name="Profiles",
            ),
        ),
        migrations.AddField(
            model_name="ressource",
            name="short_description",
            field=wagtail.core.fields.RichTextField(
                blank=True,
                help_text="Sera affiché sur la carte de la ressource",
                null=True,
                verbose_name="Description courte",
            ),
        ),
        migrations.AddField(
            model_name="ressource",
            name="source_link",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="Lien de la source"
            ),
        ),
        migrations.AddField(
            model_name="ressource",
            name="source_name",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="Nom de la source"
            ),
        ),
        migrations.CreateModel(
            name="NewsLetterSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "newsLetter",
                    models.URLField(
                        blank=True,
                        help_text="Lien d'inscription à la lettre d'information",
                        max_length=300,
                        null=True,
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.site",
                    ),
                ),
            ],
            options={
                "verbose_name": "Inscription à la lettre d'information",
            },
        ),
    ]
