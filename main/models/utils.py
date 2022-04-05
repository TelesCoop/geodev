from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


def paragraph_block(additional_field, required):
    return (
        "paragraph",
        blocks.RichTextBlock(
            label="Contenu",
            features=SIMPLE_RICH_TEXT_FIELD_FEATURE
            + ["h3", "h4", "ol", "ul"]
            + additional_field,
            required=required,
        ),
    )


SIMPLE_RICH_TEXT_FIELD_FEATURE = ["bold", "italic", "link"]
COLOR_CHOICES = (
    ("blue", "Bleue"),
    ("pink", "Rose"),
    ("white", "Blanche"),
    ("none", "Sans couleur"),
)


class FreeBodyField(models.Model):
    color_block = (
        "color",
        blocks.ChoiceBlock(
            choices=COLOR_CHOICES,
            default="none",
            help_text="Couleur de fond",
        ),
    )

    body = StreamField(
        [
            # Is h1
            (
                "heading",
                blocks.CharBlock(form_classname="full title", label="Titre de la page"),
            ),
            (
                "section",
                blocks.StructBlock(
                    [
                        color_block,
                        (
                            "image",
                            ImageChooserBlock(
                                label="Image à côté du paragraphe", required=False
                            ),
                        ),
                        (
                            "position",
                            blocks.ChoiceBlock(
                                choices=[
                                    ("right", "Droite"),
                                    ("left", "Gauche"),
                                ],
                                required=False,
                                help_text="Position de l'image",
                            ),
                        ),
                        paragraph_block(["h2"], True),
                        (
                            "sub_section",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        color_block,
                                        paragraph_block([], False),
                                        (
                                            "columns",
                                            blocks.ListBlock(
                                                blocks.StructBlock(
                                                    [
                                                        color_block,
                                                        paragraph_block([], False),
                                                    ],
                                                    label="Colonne",
                                                ),
                                                label="Colonnes",
                                            ),
                                        ),
                                    ],
                                    label="Sous section",
                                ),
                                label="Sous sections",
                            ),
                        ),
                    ],
                    label="Section",
                ),
            ),
            ("image", ImageChooserBlock()),
            ("pdf", DocumentChooserBlock()),
        ],
        blank=True,
        verbose_name="Description",
        help_text="Corps de la page",
    )

    panels = [
        StreamFieldPanel("body", classname="full"),
    ]

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    class Meta:
        abstract = True
