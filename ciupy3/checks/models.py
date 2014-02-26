from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django_pg import models

from pq.models import Job


class Check(models.Model):
    id = models.UUIDField(auto_add=True, primary_key=True)
    job = models.OneToOneField(Job)
    created_at = models.DateTimeField(default=now)
    requirements = models.TextField()

    def get_absolute_url(self):
        return reverse('check_detail', kwargs={'pk': str(self.pk)})
