from django.core.management.base import BaseCommand
from django.core.files import File
from skin_analyzer.models import Product
import os
import requests
from django.conf import settings

class Command(BaseCommand):
    help = 'Adds sample products to the database'

    def handle(self, *args, **kwargs):
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'product_images')
        os.makedirs(media_dir, exist_ok=True)

        products = [
            {
                'name': 'Botanical Repair Mist',
                'brand': 'Natural Beauty',
                'category': 'Skincare',
                'price': 29.99,
                'description': 'A gentle mist that helps repair and soothe damaged skin',
                'suitable_for': 'Dry & cracked skin, Sensitive Skin, Acne-prone Skin, Oily Skin, Dull skin, Rough skin',
                'targets': 'Dull skin, Uneven skin tone, Sebum control, Redness, Hyperpigmentation',
                'when_to_apply': 'AM PM',
                'image_url': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=500&h=500&fit=crop'
            },
            {
                'name': 'Lavender Foaming Face Wash',
                'brand': 'Pure Essentials',
                'category': 'Cleanser',
                'price': 24.99,
                'description': 'A gentle foaming cleanser with lavender extract',
                'suitable_for': 'Sensitive Skin, Acne-prone Skin, Texture, Teen Age, Fine Lines, Wrinkles, Dullness, Environmental Damage, Irritation, Normal skin, Combination skin, Oily skin, Dry skin',
                'targets': 'Dull skin, Uneven skin tone, Redness, Broken & Acne Skin, Enlarged pores, Hyperpigmentation',
                'when_to_apply': 'AM PM',
                'image_url': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=500&h=500&fit=crop'
            },
            {
                'name': 'Lavender Soothing Lotion',
                'brand': 'Pure Essentials',
                'category': 'Moisturizer',
                'price': 34.99,
                'description': 'A calming lotion with lavender extract for sensitive skin',
                'suitable_for': 'Dry & cracked skin, Dull skin, Rough skin',
                'targets': 'Dull skin, Dry Skin, Uneven skin tone, Redness, Hyperpigmentation',
                'when_to_apply': 'AM PM',
                'image_url': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=500&h=500&fit=crop'
            },
            {
                'name': 'Charcoal Detox Soap',
                'brand': 'Pure Essentials',
                'category': 'Cleanser',
                'price': 19.99,
                'description': 'A deep cleansing soap with activated charcoal',
                'suitable_for': 'Normal skin, Combination skin, Oily skin',
                'targets': 'Uneven skin tone, Broken & Acne Skin, Enlarged pores, Hyperpigmentation',
                'when_to_apply': 'AM, PM',
                'image_url': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=500&h=500&fit=crop'
            }
        ]

        for product_data in products:
            # Download image
            image_url = product_data.pop('image_url')
            image_name = f"{product_data['name'].lower().replace(' ', '_')}.jpg"
            image_path = os.path.join(media_dir, image_name)
            
            try:
                response = requests.get(image_url)
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                
                # Create product with image
                with open(image_path, 'rb') as f:
                    product = Product.objects.get_or_create(
                        name=product_data['name'],
                        defaults={
                            **product_data,
                            'image': File(f, name=image_name)
                        }
                    )
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product_data["name"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding product {product_data["name"]}: {str(e)}')) 