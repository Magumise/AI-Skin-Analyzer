import csv
from django.core.management.base import BaseCommand
from skin_analyzer.models import Product
import random

class Command(BaseCommand):
    help = 'Import products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
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
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Determine category based on product name
                category = 'Skincare'  # Default category
                if 'wash' in row['Product'].lower() or 'cleanser' in row['Product'].lower():
                    category = 'Cleanser'
                elif 'moisturizer' in row['Product'].lower() or 'lotion' in row['Product'].lower():
                    category = 'Moisturizer'
                elif 'serum' in row['Product'].lower():
                    category = 'Serum'
                elif 'mask' in row['Product'].lower():
                    category = 'Mask'
                elif 'toner' in row['Product'].lower():
                    category = 'Toner'
                elif 'scrub' in row['Product'].lower():
                    category = 'Scrub'
                
                # Get price range for category
                min_price, max_price = price_ranges.get(category, price_ranges['Skincare'])
                price = round(random.uniform(min_price, max_price), 2)
                
                # Generate random stock (between 10 and 50)
                stock = random.randint(10, 50)
                
                Product.objects.create(
                    name=row['Product'],
                    description=f"Suitable for: {row['Suitable for']}\nTargets: {row['Targets']}",
                    suitable_for=row['Suitable for'],
                    targets=row['Targets'],
                    when_to_apply=row['When to apply'],
                    price=price,
                    category=category,
                    brand='Aurora Beauty',
                    stock=stock
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully imported product: {row["Product"]} with price ${price} and stock {stock}')
                ) 