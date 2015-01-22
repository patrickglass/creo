from django.db import models


class Comp(models.Model):
    """Component heiarchy is not handled in this example
    """
    name = models.CharField(max_length=50, null=False, unique=True, db_index=True)
    alias = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    revision = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
