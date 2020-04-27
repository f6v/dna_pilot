import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dna_pilot_project.settings")

app = Celery("dna_pilot")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
