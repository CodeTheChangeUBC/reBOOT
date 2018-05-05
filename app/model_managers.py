
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class ResourceManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(ResourceManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return ResourceQuerySet(self.model).filter(deleted_at=None)
        return ResourceQuerySet(self.model)

    def destroy(self):
        return self.get_queryset().hard_delete()


class ResourceModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = ResourceManager()
    all_objects = ResourceManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def destroy(self):
        super(ResourceModel, self).delete()


class ResourceQuerySet(QuerySet):
    def delete(self):
        return super(ResourceQuerySet, self).update(deleted_at=timezone.now())

    def destroy(self):
        return super(ResourceQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)
