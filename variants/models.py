import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class UserVariant(models.Model):
    rsid = models.CharField(max_length=20)
    chromosome = models.CharField(max_length=2)
    position = models.IntegerField()
    genotype = models.CharField(max_length=2)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,)

    def publications(self):
        pass

    def __str__(self):
        return self.rsid

    def get_absolute_url(self):
        return reverse("variant_detail", kwargs={"pk": str(self.pk)})


class Recommendation(models.Model):
    rsid = models.TextField()
    text = models.TextField()


class Publication(models.Model):
    rsid = models.TextField()
    title = models.TextField()
    trait = models.TextField()
    pubmed_id = models.IntegerField()

    def pubmed_url(self):
        return "https://pubmed.ncbi.nlm.nih.gov/%d" % self.pubmed_id
