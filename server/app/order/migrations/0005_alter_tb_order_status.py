# Generated by Django 4.2.15 on 2024-09-05 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_tb_order_item_buy_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_order',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('packed', 'Packed'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='processing', max_length=250),
        ),
    ]