'''
Module for tasks to be sent on task queue
'''
import os
from celery import task
from celery.states import SUCCESS
from celery.utils.log import get_task_logger
from django.core import serializers
from django.utils import timezone as tz

from app.enums import DonationStatusEnum
from app.models import Donor, Donation, Item
from app.utils.files import render_to_pdf, generate_zip
from app.worker.app_celery import update_percent, set_complete


logger = get_task_logger(__name__)


@task
def create_receipt(queryset, total_count):
    ''' Generates PDF from queryset given in views
    '''
    donation_pks = []
    pdf_array, pdf_array_names = [], []
    row_count, previous_percent = 0, 0
    update_percent(0)
    for row in serializers.deserialize('json', queryset):
        donation = row.object
        donation_pks.append(donation.pk)
        file_context = __generate_context(donation)

        response = render_to_pdf('pdf/receipt.html', donation.pk, file_context)
        pdf_array.append(response)
        pdf_array_names.append('Tax Receipt ' + donation.pk + '.pdf')

        # Process update
        row_count += 1
        process_percent = int(100 * float(row_count) / float(total_count))
        update_percent(process_percent)

        logger.info('Generated PDF #%s ||| %s%%' % (row_count, process_percent))

    Donation.objects.filter(pk__in=donation_pks).update(
        tax_receipt_created_at=timezone.localtime(),
        status=DonationStatusEnum.RECEIPTED.name)

    set_complete()

    if len(pdf_array) == 1:
        return pdf_array[0]
    else:
        return generate_zip(pdf_array, pdf_array_names)


'''
Private Methods
'''


def __get_items_quantity_and_value(items):
    total_quant, total_value = 0, 0
    for item in items:
        total_quant += item.quantity
        total_value += item.value * item.quantity
    return total_quant, total_value


def __get_static_file_path(file_name):
    return os.path.join(os.getcwd(), 'static/admin', file_name)


def __generate_context(donation):
    items = donation.item_set.all()
    total_quant, total_value = __get_items_quantity_and_value(items)
    today_date = str(tz.localdate())

    context = {
        'logo_path': __get_static_file_path('img/reboot-logo-2.png'),
        'sign_path': __get_static_file_path('img/colin-webster.png'),
        'generated_date': today_date,
        'date': donation.donate_date,
        'donor': donation.donor,
        'tax_receipt_no': donation.pk,
        'list_of_items': items,
        'total_value': total_value,
        'total_quant': total_quant,
        'pick_up': donation.pick_up
    }
    return context
