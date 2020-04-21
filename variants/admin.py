from django.contrib import admin
from .models import Variant, Recommendation


class RecommendationInline(admin.TabularInline):
    model = Recommendation


class VariantAdmin(admin.ModelAdmin):
    inlines = [
        RecommendationInline
    ]
    list_display = ("rsid",)

admin.site.register(Variant, VariantAdmin)
