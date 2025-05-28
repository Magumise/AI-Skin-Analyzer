from django.core.management.base import BaseCommand
from skin_analyzer.models import Product
from django.db.models import Count

class Command(BaseCommand):
    help = 'Clean up duplicate products'

    def handle(self, *args, **options):
        # Find products with duplicate names
        duplicates = Product.objects.values('name').annotate(count=Count('id')).filter(count__gt=1)
        
        for duplicate in duplicates:
            name = duplicate['name']
            products = Product.objects.filter(name=name).order_by('id')
            
            # Keep the first one, delete the rest
            first_product = products.first()
            products_to_delete = products.exclude(id=first_product.id)
            
            self.stdout.write(f"Found {duplicate['count']} duplicates for product: {name}")
            self.stdout.write(f"Keeping product ID: {first_product.id}")
            
            for product in products_to_delete:
                self.stdout.write(f"Deleting product ID: {product.id}")
                product.delete()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully cleaned up duplicates for: {name}')) 