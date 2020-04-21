from django import forms


class UploadFileForm(forms.Form):
    vcf_file = forms.FileField()
