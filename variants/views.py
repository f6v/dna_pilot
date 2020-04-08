from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Variant


class VariantListView(LoginRequiredMixin, ListView):
    model = Variant
    context_object_name = 'variant_list'
    template_name = 'variants/variant_list.html'

    def get_queryset(self):
        return Variant.objects.filter(user=self.request.user)
