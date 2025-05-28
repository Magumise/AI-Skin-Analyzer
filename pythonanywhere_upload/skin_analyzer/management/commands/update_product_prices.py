from django.core.management.base import BaseCommand
from skin_analyzer.models import Product
import random

class Command(BaseCommand):
    help = 'Update product prices and quantities'

    def handle(self, *args, **options):
        # Price ranges for different categories
        price_ranges = {
            'Cleanser': (15.99, 29.99),
            'Moisturizer': (24.99, 39.99),
            'Serum': (29.99, 49.99),
            'Mask': (19.99, 34.99),
            'Toner': (14.99, 24.99),
            'Scrub': (17.99, 27.99),
            'Skincare': (19.99, 34.99),  # Default range
        }
        
        products = Product.objects.all()
        updated_count = 0
        
        for product in products:
            # Determine category based on product name
            category = 'Skincare'  # Default category
            if 'wash' in product.name.lower() or 'cleanser' in product.name.lower():
                category = 'Cleanser'
            elif 'moisturizer' in product.name.lower() or 'lotion' in product.name.lower():
                category = 'Moisturizer'
            elif 'serum' in product.name.lower():
                category = 'Serum'
            elif 'mask' in product.name.lower():
                category = 'Mask'
            elif 'toner' in product.name.lower():
                category = 'Toner'
            elif 'scrub' in product.name.lower():
                category = 'Scrub'
            
            # Get price range for category
            min_price, max_price = price_ranges.get(category, price_ranges['Skincare'])
            price = round(random.uniform(min_price, max_price), 2)
            
            # Generate random stock (between 10 and 50)
            stock = random.randint(10, 50)
            
            # Update product
            product.price = price
            product.stock = stock
            product.save()
            
            updated_count += 1
            self.stdout.write(f"Updated {product.name}: Price=${price}, Stock={stock}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} products')) 