'''
Module for tasks to be sent on task queue
'''
import os
import operator
from celery import task
from celery.states import SUCCESS
from celery.utils.log import get_task_logger
from django.core import serializers
from django.db.models import Sum, F
from django.utils import timezone as tz

from app.enums import DonationStatusEnum, ItemCategoryEnum
from app.models import Donor, Donation, Item, ItemDeviceType
from app.utils.files import render_to_pdf, generate_zip
from app.worker.app_celery import update_percent, set_success


logger = get_task_logger(__name__)


@task
def create_receipt(queryset, total_count):
    ''' Generates PDF from queryset given in views
    '''
    donation_pks = []
    pdf_array, pdf_array_names = [], []
    row_count, previous_percent = 0, 0
    update_percent(0)
    reboot_stat = __get_reboot_stat()

    for row in serializers.deserialize('json', queryset):
        donation = row.object
        donation_pks.append(donation.pk)
        context = __generate_context(donation, reboot_stat)

        response = render_to_pdf('pdf/receipt.html', donation.pk, context)
        pdf_array.append(response)
        pdf_array_names.append('Tax Receipt ' + donation.pk + '.pdf')

        # Process update
        row_count += 1
        process_percent = int(100 * float(row_count) / float(total_count))
        update_percent(process_percent)

        logger.info('Generated PDF#%s ||| %s%%' % (row_count, process_percent))

    Donation.objects.filter(pk__in=donation_pks).update(
        tax_receipt_created_at=tz.localtime(),
        status=DonationStatusEnum.RECEIPTED.name)

    set_success()

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
        total_value += float(item.value) * item.quantity
    return total_quant, total_value


def __get_static_file_path(file_name):
    return os.path.join(os.getcwd(), 'static/admin', file_name)


def __get_all_item_stat():
    return ItemDeviceType.objects.aggregate(
        sum=Sum('itemdevice__item__quantity'))['sum']


def __get_item_category_stat(category_enum):
    quantity_column = 'itemdevice__item__quantity'
    return ItemDeviceType.objects \
                         .filter(category=category_enum.name) \
                         .aggregate(sum=Sum(quantity_column))['sum']


def __get_reboot_stat():
    computers = __get_item_category_stat(ItemCategoryEnum.COMPUTER)
    printers = __get_item_category_stat(ItemCategoryEnum.PRINTER)
    monitors = __get_item_category_stat(ItemCategoryEnum.MONITOR)
    storage = __get_item_category_stat(ItemCategoryEnum.STORAGE)

    others = __get_all_item_stat() - computers - printers - monitors - storage

    return {
        'computers': computers,
        'printers': printers,
        'monitors': monitors,
        'storage': storage,
        'others': others
    }


def __get_donor_stat(donor):
    item_qs = Item.objects.none()
    for d in donor.donation_set.all():
        item_qs = item_qs | d.item_set.all()
    return item_qs.values(category=F('device__dtype__category')) \
                  .annotate(quantity=Sum('quantity')) \
                  .order_by('quantity') \
                  .values_list('category', 'quantity')[:5]


def __generate_context(donation, reboot_stat):
    items = donation.item_set.all()
    total_quant, total_value = __get_items_quantity_and_value(items)
    today_date = tz.localdate().strftime('%b %d, %Y')
    donor_stat = __get_donor_stat(donation.donor)
    number_of_padding_needed = max(15 - donation.item_set.count(), 0)

    context = {
        'reboot_stat': reboot_stat,
        'donor_stat_keys': list(donor_stat)[0:6],
        'donor_stat': donor_stat,
        'logo_path': __get_static_file_path('img/reboot-logo-2.png'),
        'sign_path': __get_static_file_path('img/colin-webster.png'),
        'footer_path': __get_static_file_path('img/reboot-footer.png'),
        'slogan_path': __get_static_file_path('img/reboot-slogan.png'),
        'css_path': __get_static_file_path('css/receipt.css'),
        'generated_date': today_date,
        'date': donation.donate_date,
        'donor': donation.donor,
        'tax_receipt_no': donation.pk,
        'list_of_items': items,
        'total_value': format(total_value, '.2f'),
        'total_quant': total_quant,
        'pick_up': donation.pick_up,
        'empty_rows': [i for i in range(number_of_padding_needed)]
    }
    return context
