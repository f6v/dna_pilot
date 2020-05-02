from django.contrib import admin
from django.urls import re_path

from .models import Publication


class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        "rsid",
        "title",
    )


admin.site.register(Publication, PublicationAdmin)
