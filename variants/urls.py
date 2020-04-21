from django.urls import path

from .views import VariantListView, VariantUploadView, VariantDetailView

urlpatterns = [
    path('', VariantListView.as_view(), name='variant_list'),
    path('upload', VariantUploadView.as_view(), name='variant_upload'),
    path('<uuid:pk>', VariantDetailView.as_view(), name='variant_detail'),
]
