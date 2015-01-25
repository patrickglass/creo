from django.conf import settings
from django.db import models


class Field(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100, db_index=True, unique=True)
    FIELD_TYPES = (
        ('S', 'str'),
        ('I', 'int'),
        ('D', 'float'),
        ('F', 'file'),
    )
    value_type = models.CharField(max_length=1, choices=FIELD_TYPES)
    default = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.name

    def __repr__ (self):
        return '<Fields %s: %s (%s)>' % (self.name, self.default, self.value_type)


class Config(models.Model):
    comp = models.ForeignKey(settings.CREO_COMPONENT_MODEL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)
    revision = models.IntegerField(default=1, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('comp', 'name', 'revision',)

    def __str__ (self):
        return self.name

    def __repr__ (self):
        return '<Config %s: %s %s>' % (self.name, self.comp, self.revision)


class Entry(models.Model):
    config = models.ForeignKey(Config)
    field = models.ForeignKey(Field)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    value = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.name

    def __repr__ (self):
        return '<Config %s: %s %s>' % (self.name, self.comp, self.revision)

    class Meta:
        unique_together = ('config', 'field', )
