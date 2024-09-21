# Generated by Django 4.2.15 on 2024-08-28 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_tb_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product.tb_product_subcategory'),
        ),
    ]
