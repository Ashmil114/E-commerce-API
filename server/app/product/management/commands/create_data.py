# Create Some Fruits and Vegetables data

from django.core.management.base import BaseCommand
from app.seller.models import tb_seller
from app.product.models import tb_product, tb_product_subcategory


class Command(BaseCommand):
    help = "Creates application data"

    def handle(self, *args, **kwargs):

        seller = tb_seller.objects.filter(user__username="atozfruits")
        seller = seller.first()
        category = tb_product_subcategory.objects.filter(title="Fruits & Vegtables")
        category = category.first()

        products = [
            {
                "title": "Orange",
                "price": 100,
                "mrp": 120,
                "fixed_quantity": 1,
                "unit": "kg",
                "stock": 50,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Banana",
                "price": 50,
                "mrp": 60,
                "fixed_quantity": 1,
                "unit": "kg",
                "stock": 100,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Beetroot",
                "price": 80,
                "mrp": 100,
                "fixed_quantity": 1,
                "unit": "kg",
                "stock": 75,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Grapes",
                "price": 120,
                "mrp": 140,
                "fixed_quantity": 1,
                "unit": "kg",
                "stock": 30,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Carrot",
                "price": 40,
                "mrp": 50,
                "fixed_quantity": 1,
                "unit": "kg",
                "stock": 200,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Broccoli",
                "price": 90,
                "mrp": 110,
                "fixed_quantity": 1,
                "unit": "kg",
                "stock": 60,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Tomato",
                "price": 30,
                "mrp": 45,
                "fixed_quantity": 500,
                "unit": "g",
                "stock": 150,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Spinach",
                "price": 55,
                "mrp": 65,
                "fixed_quantity": 250,
                "unit": "g",
                "stock": 80,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Potato",
                "price": 30,
                "mrp": 40,
                "fixed_quantity": 1,
                "unit": "kg",
                "stock": 300,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Cucumber",
                "price": 60,
                "mrp": 70,
                "fixed_quantity": 1,
                "unit": "kg",
                "stock": 120,
                "sub_category": category,
                "seller": seller,
            },
        ]

        for p in products:
            tb_product.objects.create(**p)
