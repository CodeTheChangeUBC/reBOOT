'''
Module for tasks to be sent on task queue
'''
from celery.decorators import task
from celery import Celery, current_task, shared_task
from app.models import Item
from app.utils.utils import render_to_pdf, generate_zip
import datetime

# Note for celery:
# This is using RabbitMQ. To run, must have a worker running the tasks
# Use 'celery -A reboot worker -l info'
# Then in another terminal, run 'python manage.py runserver'
# Make sure worker is running, then task will be queued by worker.

# generates PDF from queryset given in views


@shared_task
def generate_pdf(queryset):
    current_task.update_state(
        state='STARTING',
        meta={
            'state': 'STARTING',
            'process_percent': 0})
    # Forward Variable declaration
    pdf_array = []
    pdf_array_names = []
    total_row_count = sum(1 for line in queryset)
    row_count, previous_percent = 0, 0
    for row in queryset:
        listofitems = Item.objects.select_related().filter(
            tax_receipt_no=row.tax_receipt_no)

        totalvalue, totalquant = 0, 0
        for item in listofitems:
            totalvalue += item.value * item.quantity
            totalquant += item.quantity
        today = datetime.date.today()
        today_date = str(today.year) + "-" + \
            str(today.month) + "-" + str(today.day)
        data = {
            'generated_date': today_date,
            'date': row.donate_date,
            'donor': row.donor_id,
            'tax_receipt_no': row.tax_receipt_no,
            'listofitems': listofitems,
            'totalvalue': totalvalue,
            'totalquant': totalquant,
            'pick_up': row.pick_up
        }
        response = render_to_pdf('pdf/receipt.html', row.tax_receipt_no, data)
        pdf_array.append(response)
        pdf_array_names.append("Tax Receipt " + row.tax_receipt_no + ".pdf")
        row_count += 1
        process_percent = int(100 * float(row_count) / float(total_row_count))
        current_task.update_state(
            state='PROGRESS',
            meta={
                'state': 'PROGRESS',
                'process_percent': process_percent})
        print(
            "Generated PDF #" +
            str(row_count) +
            " ||| Percent = " +
            str(process_percent))
    current_task.update_state(
        state='COMPLETE',
        meta={
            'state': 'COMPLETE',
            'process_percent': 100})
    if (len(pdf_array) == 1):
        return pdf_array[0]
    else:
            # generate_zip defined in utils.py
        return generate_zip(pdf_array, pdf_array_names)
