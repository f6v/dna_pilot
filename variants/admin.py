from django.contrib import admin
from django.urls import re_path

from .models import Publication, Recommendation


class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        "rsid",
        "title",
    )

class RecommendationAdmin(admin.ModelAdmin):
    list_display = (
        "rsid",
        "text",
    )


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
