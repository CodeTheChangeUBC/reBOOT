from django.contrib.admin import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe


class CustomForeignKeyRawIdWidget(widgets.ForeignKeyRawIdWidget):
    template_name = "admin/widgets/custom_foreign_key_raw_id.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        rel_to = self.rel.model
        if rel_to in self.admin_site._registry:
            # The related object is registered with the same AdminSite
            related_add_url = reverse(
                'admin:%s_%s_changelist' % (
                    rel_to._meta.app_label,
                    rel_to._meta.model_name,
                ),
                current_app=self.admin_site.name,
            )
            related_add_url += 'add/'

            params = self.url_parameters()
            if params:
                related_add_url += '?' + \
                    '&amp;'.join('%s=%s' % (k, v) for k, v in params.items())
            context['related_add_url'] = mark_safe(related_add_url)
        return context
