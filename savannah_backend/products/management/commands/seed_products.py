from django.core.management.base import BaseCommand
from products.models import Category, Product
import random

class Command(BaseCommand):
    help = "Seed categories and products"

    def handle(self, *args, **kwargs):
        # Clear existing data (optional)
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Level 1
        all_products = Category.objects.create(name="All Products")

        # Level 2
        bakery = Category.objects.create(name="Bakery", parent=all_products)
        produce = Category.objects.create(name="Produce", parent=all_products)

        # Level 3
        bread = Category.objects.create(name="Bread", parent=bakery)
        cookies = Category.objects.create(name="Cookies", parent=bakery)
        fruits = Category.objects.create(name="Fruits", parent=produce)
        vegetables = Category.objects.create(name="Vegetables", parent=produce)

        # Add some products
        Product.objects.create(name="White Bread", price=70.0, category=bread)
        Product.objects.create(name="Whole Wheat Bread", price=80.0, category=bread)
        Product.objects.create(name="Chocolate Chip Cookies", price=100.0, category=cookies)
        Product.objects.create(name="Oatmeal Cookies", price=90.0, category=cookies)
        Product.objects.create(name="Apple", price=50.0, category=fruits)
        Product.objects.create(name="Banana", price=30.0, category=fruits)
        Product.objects.create(name="Carrot", price=20.0, category=vegetables)
        Product.objects.create(name="Spinach", price=25.0, category=vegetables)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
