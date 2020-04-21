import logging
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse

from .forms import UploadFileForm
from .models import Variant, UserVariant
from .variants_processing import handle_uploaded_file


logger = logging.getLogger(__name__)

class VariantListView(LoginRequiredMixin, ListView):
    model = UserVariant
    context_object_name = 'user_variant_list'
    template_name = 'variants/variant_list.html'

    def get_queryset(self):
        return UserVariant.objects.select_related('variant').filter(user=self.request.user)

class VariantUploadView(LoginRequiredMixin, TemplateView):
    template_name = 'variants/variant_upload.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['vcf_file'], request.user)
            return HttpResponseRedirect(reverse('variant_list'))

        return render(request, self.template_name)

class VariantDetailView(LoginRequiredMixin, DetailView):
    model = UserVariant
    context_object_name = 'variant'
    template_name = 'variants/variant_detail.html'
