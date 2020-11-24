from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.functions import Now

from model_utils.managers import QueryManager
from model_utils.models import StatusModel, TimeFramedModel, TimeStampedModel
from model_utils import Choices


User = get_user_model()
now = Now()


class System(models.Model):
    name = models.CharField(max_length=200)

    def has_incident(self):
        return Incident.timeframed.filter(system=self).exists()

    def get_incident(self):
        return Incident.timeframed.filter(system=self).first()

    def __str__(self):
        return self.name


class Incident(StatusModel, TimeFramedModel, TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    STATUS = Choices('maintenance', 'partial_outage', 'major_outage')
    opened_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    system = models.ForeignKey(System, on_delete=models.CASCADE)

    objects = models.Manager()

    active = QueryManager(
        (models.Q(start__lte=now) | models.Q(start__isnull=True))
        & (models.Q(end__gte=now) | models.Q(end__isnull=True))
    )

    closed = QueryManager(
        models.Q(end__lte=now)
    )

    def __str__(self):
        return f"{self.system} - {self.status} [{self.start}:{self.end}]"
