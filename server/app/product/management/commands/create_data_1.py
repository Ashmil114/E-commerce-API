from django.core.management.base import BaseCommand
from app.seller.models import tb_seller
from app.product.models import tb_product, tb_product_subcategory


class Command(BaseCommand):
    help = "Creates application data"

    def handle(self, *args, **kwargs):

        seller = tb_seller.objects.filter(user__username="hibasupermarket")
        seller = seller.first()
        category = tb_product_subcategory.objects.filter(title="Tea, Coffee and More")
        category = category.first()

        products = [
            {
                "title": "Tea",
                "price": 30,
                "mrp": 40,
                "fixed_quantity": 200,
                "unit": "g",
                "stock": 200,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Green Tea",
                "price": 35,
                "mrp": 45,
                "fixed_quantity": 100,
                "unit": "g",
                "stock": 180,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Coffee",
                "price": 45,
                "mrp": 55,
                "fixed_quantity": 100,
                "unit": "g",
                "stock": 150,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Bru Coffee",
                "price": 50,
                "mrp": 60,
                "fixed_quantity": 100,
                "unit": "g",
                "stock": 140,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Horlicks",
                "price": 80,
                "mrp": 100,
                "fixed_quantity": 500,
                "unit": "g",
                "stock": 100,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Boost",
                "price": 90,
                "mrp": 110,
                "fixed_quantity": 500,
                "unit": "g",
                "stock": 120,
                "sub_category": category,
                "seller": seller,
            },
            {
                "title": "Bornvita",
                "price": 85,
                "mrp": 105,
                "fixed_quantity": 500,
                "unit": "g",
                "stock": 130,
                "sub_category": category,
                "seller": seller,
            },
        ]

        for p in products:
            tb_product.objects.create(**p)
