import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Variant(models.Model):
    rsid = models.CharField(max_length=20, unique=True)
    chromosome = models.CharField(max_length=2)
    position = models.IntegerField()

    def __str__(self):
        return self.rsid

class UserVariant(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
    )
    genotype = models.CharField(max_length=2)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        #related_name='user_variants',
    )

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]

    def position(self):
        return self.variant.position

    def chromosome(self):
        return self.variant.chromosome

    def rsid(self):
        return self.variant.rsid

    def recommendations(self):
        return self.variant.recommendations.all()

    def publications(self):
        return self.variant.publications.all()

    def __str__(self):
        return self.rsid

    def get_absolute_url(self):
        return reverse('variant_detail', kwargs={'pk': str(self.pk)})


class Recommendation(models.Model):
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    text = models.CharField(max_length=300)


class Publication(models.Model):
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name='publications'
    )
    text = models.CharField(max_length=300)
    trait = models.CharField(max_length=300)
    pubmed_id = models.IntegerField()

    def pubmed_url(self):
        return 'https://pubmed.ncbi.nlm.nih.gov/%d' % self.pubmed_id
