'''
Module for tasks to be sent on task queue
'''
import os
from celery import task
from celery.states import SUCCESS
from django.core import serializers
from django.utils import timezone

from app.models import Donor, Donation, Item
from app.utils.utils import render_to_pdf, generate_zip
from app.worker.app_celery import update_percent, set_complete


@task
def generate_pdf(queryset, total_count):
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

        print('Generated PDF #%s ||| %s%%' % (row_count, process_percent))

    Donation.objects.filter(pk__in=donation_pks).update(
        tax_receipt_created_at=timezone.localtime())

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


def __generate_context(donation):
    items = Item.objects.filter(donation__tax_receipt_no=donation.pk)
    total_quant, total_value = __get_items_quantity_and_value(items)
    today_date = str(timezone.localdate())

    context = {
        'logo_path': os.path.join(os.getcwd(), 'static/admin/img', 'reboot-logo-2.png'),
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
