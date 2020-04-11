import logging
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from .models import Variant


logger = logging.getLogger(__name__)

class VariantListView(LoginRequiredMixin, ListView):
    model = Variant
    context_object_name = 'variant_list'
    template_name = 'variants/variant_list.html'

    def get_queryset(self):
        return Variant.objects.filter(user=self.request.user)

class VariantUploadView(LoginRequiredMixin, TemplateView):
    template_name = 'variants/variant_upload.html'

    def get(self, request):
        logger.info('pizda')
        return render(request, self.template_name)

    def post(self, request):
        logger.info("hui")
        logger.info(request.FILES)
        return render(request, self.template_name)
