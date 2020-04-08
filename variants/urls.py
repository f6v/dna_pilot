from django.urls import path

from .views import VariantListView

urlpatterns = [
    path('', VariantListView.as_view(), name='variants_list'),
]
