# Generated by Django 3.2.11 on 2022-03-18 11:17

import datetime
from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.routable_page.models
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0023_add_choose_permissions"),
        ("wagtailcore", "0066_collection_management_permissions"),
        ("main", "0003_map_ressource"),
    ]

    operations = [
        migrations.CreateModel(
            name="ActualityType",
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
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="name"),
                ),
                (
                    "slug",
                    models.SlugField(max_length=100, unique=True, verbose_name="slug"),
                ),
            ],
            options={
                "verbose_name": "Type d'actualité",
                "verbose_name_plural": "Types d'actualité",
            },
        ),
        migrations.CreateModel(
            name="NewsListPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "verbose_name": "Page des actualités",
                "verbose_name_plural": "Pages des actualités",
            },
            bases=(
                wagtail.contrib.routable_page.models.RoutablePageMixin,
                "wagtailcore.page",
            ),
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Profil",
                "verbose_name_plural": "Profils",
            },
        ),
        migrations.CreateModel(
            name="RessourcesPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "verbose_name": "Page des ressources",
                "verbose_name_plural": "Pages des ressources",
            },
            bases=(
                wagtail.contrib.routable_page.models.RoutablePageMixin,
                "wagtailcore.page",
            ),
        ),
        migrations.CreateModel(
            name="Thematic",
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
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="name"),
                ),
                (
                    "slug",
                    models.SlugField(max_length=100, unique=True, verbose_name="slug"),
                ),
            ],
            options={
                "verbose_name": "Thématique",
                "verbose_name_plural": "Thématiques",
            },
        ),
        migrations.AlterModelOptions(
            name="ressource",
            options={
                "ordering": ["-created"],
                "verbose_name": "Ressource",
                "verbose_name_plural": "Ressources",
            },
        ),
        migrations.AddField(
            model_name="ressource",
            name="slug",
            field=models.SlugField(
                default="",
                max_length=100,
                unique=True,
                verbose_name="Slug (URL de la ressource)",
            ),
        ),
        migrations.AlterField(
            model_name="ressource",
            name="country",
            field=models.CharField(
                choices=[
                    ("Afrique du Sud", "Afrique du Sud"),
                    ("Algérie", "Algérie"),
                    ("Angola", "Angola"),
                    ("Bénin", "Bénin"),
                    ("Botswana", "Botswana"),
                    ("Burkina Faso", "Burkina Faso"),
                    ("Burundi", "Burundi"),
                    ("Cameroun", "Cameroun"),
                    ("Cap-Vert", "Cap-Vert"),
                    ("République centrafricaine", "République centrafricaine"),
                    ("Comores", "Comores"),
                    ("République du Congo", "République du Congo"),
                    (
                        "République démocratique du Congo",
                        "République démocratique du Congo",
                    ),
                    ("Côte d'Ivoire", "Côte d'Ivoire"),
                    ("Djibouti", "Djibouti"),
                    ("Égypte", "Égypte"),
                    ("Érythrée", "Érythrée"),
                    ("Swaziland", "Eswatini"),
                    ("Éthiopie", "Éthiopie"),
                    ("Gabon", "Gabon"),
                    ("Gambie", "Gambie"),
                    ("Ghana", "Ghana"),
                    ("Guinée", "Guinée"),
                    ("Guinée-Bissau", "Guinée-Bissau"),
                    ("Guinée équatoriale", "Guinée équatoriale"),
                    ("Kenya", "Kenya"),
                    ("Lesotho", "Lesotho"),
                    ("Liberia", "Liberia"),
                    ("Libye", "Libye"),
                    ("Madagascar", "Madagascar"),
                    ("Malawi", "Malawi"),
                    ("Mali", "Mali"),
                    ("Maroc", "Maroc"),
                    ("Maurice", "Maurice"),
                    ("Mauritanie", "Mauritanie"),
                    ("Mozambique", "Mozambique"),
                    ("Namibie", "Namibie"),
                    ("Niger", "Niger"),
                    ("Nigeria", "Nigeria"),
                    ("Ouganda", "Ouganda"),
                    ("Rwanda", "Rwanda"),
                    ("São Tomé-et-Principe", "São Tomé-et-Principe"),
                    ("Sénégal", "Sénégal"),
                    ("Seychelles", "Seychelles"),
                    ("Sierra Leone", "Sierra Leone"),
                    ("Somalie", "Somalie"),
                    ("Soudan", "Soudan"),
                    ("Soudan du Sud", "Soudan du Sud"),
                    ("Tanzanie", "Tanzanie"),
                    ("Tchad", "Tchad"),
                    ("Togo", "Togo"),
                    ("Tunisie", "Tunisie"),
                    ("Zambie", "Zambie"),
                    ("Zimbabwe", "Zimbabwe"),
                    ("Tanzanie", "Tanzanie"),
                    ("Tchad", "Tchad"),
                    ("Togo", "Togo"),
                    ("Tunisie", "Tunisie"),
                    ("Zambie", "Zambie"),
                    ("Zimbabwe", "Zimbabwe"),
                    ("Tanzanie", "Tanzanie"),
                    ("Tchad", "Tchad"),
                    ("Togo", "Togo"),
                    ("Tunisie", "Tunisie"),
                    ("Zambie", "Zambie"),
                    ("Zimbabwe", "Zimbabwe"),
                ],
                max_length=50,
                verbose_name="Pays",
            ),
        ),
        migrations.AlterField(
            model_name="ressource",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="ressource",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Nom"),
        ),
        migrations.CreateModel(
            name="News",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="nom")),
                (
                    "publication_date",
                    models.DateTimeField(
                        default=datetime.datetime.now,
                        help_text="Permet de trier l'ordre d'affichage dans la page des actualités",
                        verbose_name="Date de publication",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        default="",
                        max_length=100,
                        unique=True,
                        verbose_name="Slug (URL de l'actualité)",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "types",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Permet le filtrage des actualités",
                        related_name="news",
                        to="main.ActualityType",
                        verbose_name="Type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Actualité / Evènement",
                "verbose_name_plural": "Actualités / Evènements",
                "ordering": ["-publication_date"],
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.AddField(
            model_name="ressource",
            name="thematics",
            field=models.ManyToManyField(
                blank=True,
                related_name="ressources",
                to="main.Thematic",
                verbose_name="Thématiques",
            ),
        ),
    ]
