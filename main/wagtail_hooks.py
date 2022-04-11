from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks

from main.models.models import Profile, Thematic, ActualityType, ResourceType
from main.models.resource import Resource
from main.models.news import News


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/geodev-admin.css to the admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/geodev-admin.css")
    )


class ProfileModelAdmin(ModelAdmin):
    model = Profile
    menu_label = "Profile type"
    menu_order = 200
    menu_icon = "group"
    add_to_settings_menu = False
    search_fields = ("name",)


class RessourceModelAdmin(ModelAdmin):
    model = Resource
    menu_label = "Ressources"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)


class ThematicModelAdmin(ModelAdmin):
    model = Thematic
    menu_label = "Thématiques"
    menu_icon = "tag"
    add_to_settings_menu = False
    search_fields = ("name",)


class ResourceTypeModelAdmin(ModelAdmin):
    model = ResourceType
    menu_label = "Types de ressource"
    menu_icon = "tag"
    add_to_settings_menu = False
    search_fields = ("name",)


class RessourcesAdminGroup(ModelAdminGroup):
    menu_label = "Ressources"
    menu_order = 201
    menu_icon = "doc-full"
    items = (RessourceModelAdmin, ThematicModelAdmin, ResourceTypeModelAdmin)


class NewsModelAdmin(ModelAdmin):
    model = News
    menu_label = "Actualités"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)


class ActualityTypeModelAdmin(ModelAdmin):
    model = ActualityType
    menu_label = "Types d'actualité"
    menu_icon = "tag"
    add_to_settings_menu = False
    form_fields_exclude = ("slug",)
    search_fields = ("name",)


class ActualityAdminGroup(ModelAdminGroup):
    menu_label = "Actualités"
    menu_order = 202
    menu_icon = "date"
    items = (NewsModelAdmin, ActualityTypeModelAdmin)


modeladmin_register(RessourcesAdminGroup)
modeladmin_register(ActualityAdminGroup)
modeladmin_register(ProfileModelAdmin)
