from django.urls import path

from .views import VariantListView, VariantUploadView

urlpatterns = [
    path('', VariantListView.as_view(), name='variants_list'),
    path('upload', VariantUploadView.as_view(), name='variant_upload'),
]
