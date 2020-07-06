# Generated by Django 2.2.10 on 2020-07-04 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20200625_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'permissions': (('generate_tax_receipt', 'Can generate tax receipts'),)},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'permissions': (('update_status_item', 'Can update item status'), ('update_value_item', 'Can update item value'))},
        ),
        migrations.AddField(
            model_name='donation',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
    ]