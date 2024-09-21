from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.seller.models import tb_seller, tb_shop_category


class Command(BaseCommand):
    help = "Creates application data"

    def handle(self, *args, **kwargs):

        tb_shop_category.objects.get_or_create(name="stationery")
        tb_shop_category.objects.get_or_create(name="Fruits and Vegtables")

        sellers = [
            {
                "user": User.objects.create(username="kbstore", password="Sample@123"),
                "phone": "7412589630",
                "shop_name": "KB Store",
                "owner_name": "Mathav",
                "category": tb_shop_category.objects.get(name="stationery"),
                "district": "Wayanad",
                "city": "Vaduvanchal",
                "pincode": "673581",
            },
            {
                "user": User.objects.create(
                    username="hibasupermarket", password="Sample@123"
                ),
                "phone": "7896541230",
                "shop_name": "Hiba Supermarket",
                "owner_name": "Jobin",
                "category": tb_shop_category.objects.get(name="stationery"),
                "district": "Wayanad",
                "city": "Kalpetta",
                "pincode": "673121",
            },
            {
                "user": User.objects.create(
                    username="atozfruits", password="Sample@123"
                ),
                "phone": "9632587410",
                "shop_name": "A to Z Fruits",
                "owner_name": "Jack",
                "category": tb_shop_category.objects.get(name="Fruits and Vegtables"),
                "district": "Wayanad",
                "city": "Meppadi",
                "pincode": "673577",
            },
        ]

        for s in sellers:
            tb_seller.objects.create(**s)
