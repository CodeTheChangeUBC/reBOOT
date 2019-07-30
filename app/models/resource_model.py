from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from datetime import datetime, date
import simplejson as json
import re


class ResourceManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(ResourceManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return ResourceQuerySet(self.model).alive()
        return ResourceQuerySet(self.model)

    def destroy(self):
        return self.get_queryset().hard_delete()


class ResourceModel(models.Model):
    created_at = models.DateTimeField(default=timezone.localtime)
    documented_at = models.CharField(
        "Date Created in Y-M-D", max_length=10, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = ResourceManager()
    all_objects = ResourceManager(alive_only=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.documented_at:
            self.documented_at = timezone.localdate().strftime("%Y-%m-%d")
        super(ResourceModel, self).save(*args, **kwargs)

    def underscore_serialize(self):
        return _underscore_serialize(self)

    def camel_serialize(self):
        return _camel_serialize(self)

    def delete(self):
        self.deleted_at = datetime.utcnow()
        self.save()

    def destroy(self):
        super(ResourceModel, self).delete()


class ResourceQuerySet(QuerySet):
    def delete(self):
        return super(ResourceQuerySet, self).update(deleted_at=timezone.localtime())

    def destroy(self):
        return super(ResourceQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


'''
Private Method
'''


def _underscore_serialize(self):
    serialized_dict = self.__dict__
    if '_state' in serialized_dict:
        serialized_dict.pop('_state')
    json_str = json.dumps(serialized_dict, default=_json_serial)
    return json.loads(json_str)


def _camel_serialize(self):
    serialized_dict = self.__dict__
    if '_state' in serialized_dict:
        serialized_dict.pop('_state')
    cameled_dict = _convert_json(serialized_dict, _underscore_to_camel)
    json_str = json.dumps(cameled_dict, default=_json_serial)
    return json.loads(json_str)


def _convert_json(d, convert):
    new_d = {}
    for k, v in d.items():
        v = v if not isinstance(v, dict) else _convert_json(v, convert)
        new_d[convert(k)] = v
    return new_d


def _underscore_to_camel(name):
    under_pat = re.compile(r'_([a-z])')
    return under_pat.sub(lambda x: x.group(1).upper(), name)


def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, ResourceModel):
        return obj.pk
    raise TypeError("Type %s not serializable" % type(obj))
