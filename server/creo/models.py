from django.conf import settings
from django.db import models


class Fields(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100, db_index=True)
    FIELD_TYPES = (
        ('S', 'str'),
        ('I', 'int'),
        ('D', 'float'),
        ('F', 'file'),
    )
    value_type = models.CharField(max_length=1, choices=FIELD_TYPES)
    default = models.TextField()

    description = models.TextField()
    is_active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)


class Config(models.Model):
    comp = models.ForeignKey(settings.CREO_COMPONENT_MODEL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    revision = models.CharField(max_length=100, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)


class Entries(models.Model):
    config = models.ForeignKey(Config)
    field = models.ForeignKey(Fields)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    value = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
