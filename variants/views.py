import logging
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .forms import UploadFileForm
from .models import UserVariant, Recommendation, Publication
from .tasks import process_vcf
from .object_storage import save_vcf


logger = logging.getLogger(__name__)


class VariantListView(LoginRequiredMixin, ListView):
    model = UserVariant
    context_object_name = "user_variant_list"
    template_name = "variants/variant_list.html"

    class Meta:
        ordering = ['id']

    def get_queryset(self):
        user_variants = UserVariant.objects.filter(user=self.request.user).order_by("id")
        paginator = Paginator(user_variants, 20)
        page = self.request.GET.get("page")

        return paginator.get_page(page)


class VariantUploadView(LoginRequiredMixin, TemplateView):
    template_name = "variants/variant_upload.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            vcf_file = request.FILES["vcf_file"]
            vcf_uid = save_vcf(vcf_file)
            process_vcf.delay(vcf_uid, request.user.id)

            return HttpResponseRedirect(reverse("variant_list"))

        return render(request, self.template_name)


class VariantDetailView(LoginRequiredMixin, DetailView):
    model = UserVariant
    context_object_name = "variant"
    template_name = "variants/variant_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        has_premium = self.request.user.has_perm('variants.premium_status')
        if not has_premium:
            context["prompt_purchase_premium"] = True

        context["recommendations"] = Recommendation.objects.filter(
            rsid=self.object.rsid
        )
        context['publications'] = Publication.objects.filter(
            rsid=self.object.rsid
        )

        return context
