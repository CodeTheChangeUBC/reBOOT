'''
Module for tasks to be sent on task queue
'''
from celery import Celery, current_task, shared_task
from celery.decorators import task
import datetime

from app.models import Item
from app.utils.utils import render_to_pdf, generate_zip


@shared_task
def generate_pdf(queryset):
    ''' Generates PDF from queryset given in views
    '''
    pdf_array, pdf_array_names = [], []
    row_count, previous_percent = 0, 0
    total_row_count = sum(1 for line in queryset)

    for row in queryset:
        file_context = __generate_context(row)

        response = render_to_pdf(
            'pdf/receipt.html', row.tax_receipt_no, file_context)
        pdf_array.append(response)
        pdf_array_names.append('Tax Receipt ' + row.tax_receipt_no + '.pdf')

        # Process update
        row_count += 1
        process_percent = int(100 * float(row_count) / float(total_row_count))
        current_task.update_state(
            state='PROGRESS',
            meta={
                'state': 'PROGRESS',
                'process_percent': process_percent
            }
        )
        print(('Generated PDF #' + str(row_count) +
              ' ||| Percent = ' + str(process_percent)))

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


def __generate_context(row):
    items = Item.objects.filter(donation__tax_receipt_no=row.tax_receipt_no)
    total_quant, total_value = __get_items_quantity_and_value(items)
    today_date = str(datetime.date.today())
    context = {
        'generated_date': today_date,
        'date': row.donate_date,
        'donor': row.donor,
        'tax_receipt_no': row.tax_receipt_no,
        'list_of_items': items,
        'total_value': total_value,
        'total_quant': total_quant,
        'pick_up': row.pick_up
    }
    return context
