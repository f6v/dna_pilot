import uuid
from django.contrib.auth import get_user_model
from django.db import models


class Variant(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    rsid = models.CharField(max_length=20)
    chromosome = models.CharField(max_length=2)
    position = models.IntegerField()
    genotype = models.CharField(max_length=2)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]

    def __str__(self):
        return self.rsid

    # def get_absolute_url(self):
    #     return reverse('book_detail', kwargs={'pk': str(self.pk)})
