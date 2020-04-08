from django.contrib import admin
from .models import Variant


class VariantAdmin(admin.ModelAdmin):
    list_display = ("rsid",)

admin.site.register(Variant, VariantAdmin)
