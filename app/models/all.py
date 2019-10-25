from django.db import models


class All(models.Model):

    class Meta:
        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model.
        default_permissions = ()
        permissions = (('can_import_historical', 'Can import historical data'),
                       ('can_import_third_party', 'Can import third party data'),
                       ('can_import_website', 'Can import website data'),
                       ('can_export_data', 'Can export data'),)
