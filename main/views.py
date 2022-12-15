import csv

# from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from main.models import Resource


def download_csv(request, queryset):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise PermissionDenied

    model = queryset.model
    model_fields = model._meta.fields + model._meta.many_to_many
    field_names = [field.name for field in model_fields]
    field_verbose_names = [
        field.verbose_name if hasattr(field, "verbose_name") else field.name
        for field in model_fields
    ]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="export.csv"'

    # the csv writer
    writer = csv.writer(response, delimiter=";")

    # Write a first row with header information
    writer.writerow(field_verbose_names)

    # Write data rows
    for row in queryset:
        values = []
        for field in field_names:
            value = getattr(row, field)
            if hasattr(value, "all"):
                value = ", ".join(str(e) for e in value.all())
            elif callable(value):
                try:
                    value = value() or ""
                except Exception:
                    value = "Error retrieving value"
            if value is None:
                value = ""
            values.append(value)
        writer.writerow(values)
    return response


def export_resources(request):
    return download_csv(request, Resource.objects.all())
