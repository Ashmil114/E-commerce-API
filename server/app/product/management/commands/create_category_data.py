from django.core.management.base import BaseCommand
from app.product.models import tb_product_subcategory, tb_product_category


class Command(BaseCommand):
    help = "Creates application data"

    def handle(self, *args, **kwargs):

        categories = [
            {"title": "Fruits & Vegtables"},
            {"title": "Snacks & Drinks"},
            {"title": "Dairy & Eggs"},
            {"title": "Cleaning & Household"},
            {"title": "Beauty & Personal Care"},
            {"title": "Electronics"},
            {"title": "Sports & Outdoors"},
            {"title": "Toys & Games"},
        ]

        for c in categories:
            tb_product_category.objects.create(**c)

        subcategories = [
            # Subcategories for "Snacks & Drinks"
            {
                "title": "Chocolates & Candies",
                "category": tb_product_category.objects.get(title="Snacks & Drinks"),
            },
            {
                "title": "Tea, Coffee and More",
                "category": tb_product_category.objects.get(title="Snacks & Drinks"),
            },
            {
                "title": "Chips & Crisps",
                "category": tb_product_category.objects.get(title="Snacks & Drinks"),
            },
            {
                "title": "Nuts & Dried Fruits",
                "category": tb_product_category.objects.get(title="Snacks & Drinks"),
            },
            {
                "title": "Soft Drinks",
                "category": tb_product_category.objects.get(title="Snacks & Drinks"),
            },
            {
                "title": "Juices & Smoothies",
                "category": tb_product_category.objects.get(title="Snacks & Drinks"),
            },
            # Subcategories for "Dairy & Eggs"
            {
                "title": "Milk & Cream",
                "category": tb_product_category.objects.get(title="Dairy & Eggs"),
            },
            {
                "title": "Cheese",
                "category": tb_product_category.objects.get(title="Dairy & Eggs"),
            },
            {
                "title": "Yogurt",
                "category": tb_product_category.objects.get(title="Dairy & Eggs"),
            },
            {
                "title": "Butter & Margarine",
                "category": tb_product_category.objects.get(title="Dairy & Eggs"),
            },
            {
                "title": "Eggs",
                "category": tb_product_category.objects.get(title="Dairy & Eggs"),
            },
            # Subcategories for "Cleaning & Household"
            {
                "title": "Laundry Detergents",
                "category": tb_product_category.objects.get(
                    title="Cleaning & Household"
                ),
            },
            {
                "title": "Dishwashing Liquid",
                "category": tb_product_category.objects.get(
                    title="Cleaning & Household"
                ),
            },
            {
                "title": "Cleaning Tools",
                "category": tb_product_category.objects.get(
                    title="Cleaning & Household"
                ),
            },
            {
                "title": "Trash Bags & Bins",
                "category": tb_product_category.objects.get(
                    title="Cleaning & Household"
                ),
            },
            {
                "title": "Paper Products",
                "category": tb_product_category.objects.get(
                    title="Cleaning & Household"
                ),
            },
            # Subcategories for "Beauty & Personal Care"
            {
                "title": "Skincare",
                "category": tb_product_category.objects.get(
                    title="Beauty & Personal Care"
                ),
            },
            {
                "title": "Haircare",
                "category": tb_product_category.objects.get(
                    title="Beauty & Personal Care"
                ),
            },
            {
                "title": "Makeup",
                "category": tb_product_category.objects.get(
                    title="Beauty & Personal Care"
                ),
            },
            {
                "title": "Personal Hygiene",
                "category": tb_product_category.objects.get(
                    title="Beauty & Personal Care"
                ),
            },
            {
                "title": "Fragrances",
                "category": tb_product_category.objects.get(
                    title="Beauty & Personal Care"
                ),
            },
            # Subcategories for "Electronics"
            {
                "title": "Mobile Phones",
                "category": tb_product_category.objects.get(title="Electronics"),
            },
            {
                "title": "Laptops & Computers",
                "category": tb_product_category.objects.get(title="Electronics"),
            },
            {
                "title": "Headphones & Earphones",
                "category": tb_product_category.objects.get(title="Electronics"),
            },
            {
                "title": "Televisions",
                "category": tb_product_category.objects.get(title="Electronics"),
            },
            {
                "title": "Smart Home Devices",
                "category": tb_product_category.objects.get(title="Electronics"),
            },
            # Subcategories for "Sports & Outdoors"
            {
                "title": "Fitness Equipment",
                "category": tb_product_category.objects.get(title="Sports & Outdoors"),
            },
            {
                "title": "Outdoor Gear",
                "category": tb_product_category.objects.get(title="Sports & Outdoors"),
            },
            {
                "title": "Camping & Hiking",
                "category": tb_product_category.objects.get(title="Sports & Outdoors"),
            },
            {
                "title": "Cycling",
                "category": tb_product_category.objects.get(title="Sports & Outdoors"),
            },
            {
                "title": "Sports Apparel",
                "category": tb_product_category.objects.get(title="Sports & Outdoors"),
            },
            # Subcategories for "Toys & Games"
            {
                "title": "Action Figures",
                "category": tb_product_category.objects.get(title="Toys & Games"),
            },
            {
                "title": "Board Games",
                "category": tb_product_category.objects.get(title="Toys & Games"),
            },
            {
                "title": "Puzzles",
                "category": tb_product_category.objects.get(title="Toys & Games"),
            },
            {
                "title": "Dolls & Stuffed Animals",
                "category": tb_product_category.objects.get(title="Toys & Games"),
            },
            {
                "title": "Building Sets",
                "category": tb_product_category.objects.get(title="Toys & Games"),
            },
            {
                "title": "Fruits & Vegtables",
                "category": tb_product_category.objects.get(title="Fruits & Vegtables"),
            },
        ]

        for s in subcategories:
            tb_product_subcategory.objects.create(**s)
