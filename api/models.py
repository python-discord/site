from django.db import models


class SnakeName(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    scientific = models.CharField(max_length=150)
