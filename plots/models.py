from django.db import models
from django.contrib.auth.models import User
import uuid

class Plot(models.Model):
    plot_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plot_name = models.CharField(max_length=255)
    plot_legend = models.JSONField()
    plot_center_coordinates = models.JSONField(default=list)  # updated default to list
    plot_geojson = models.JSONField()
    plot_heatmap_url = models.URLField()
    users = models.ManyToManyField(User, related_name='plots')

    def __str__(self):
        return self.plot_name