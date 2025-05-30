from django.core.management.base import BaseCommand
from skin_analyzer.models import Product

class Command(BaseCommand):
    help = 'Add all skincare products to the database'

    def handle(self, *args, **options):
        products = [
            {
                'name': 'Botanical Repair Mist',
                'brand': 'Aurora Beauty',
                'category': 'Toner',
                'description': 'A soothing mist that helps repair and rejuvenate skin.',
                'price': 24.99,
                'stock': 50,
                'suitable_for': 'Acne, Eczema, Rosacea, Dry Skin, Normal Skin',
                'targets': 'Skin Repair, Hydration, Soothing',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'Lavender Foaming Face Wash',
                'brand': 'Aurora Beauty',
                'category': 'Cleanser',
                'description': 'Gentle foaming cleanser with lavender extract.',
                'price': 19.99,
                'stock': 45,
                'suitable_for': 'Acne, Rosacea, Oily Skin',
                'targets': 'Cleansing, Oil Control',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'Sandal Mist',
                'brand': 'Aurora Beauty',
                'category': 'Toner',
                'description': 'Refreshing mist with sandalwood extract.',
                'price': 22.99,
                'stock': 40,
                'suitable_for': 'Acne, Rosacea, Dry Skin, Normal Skin',
                'targets': 'Hydration, Soothing',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'BIO Enzyme GLYCOLIC Vinegar',
                'brand': 'Aurora Beauty',
                'category': 'Treatment',
                'description': 'Exfoliating treatment with glycolic acid.',
                'price': 29.99,
                'stock': 35,
                'suitable_for': 'Acne, Keratosis, Milia, Oily Skin',
                'targets': 'Exfoliation, Brightening',
                'when_to_apply': 'PM'
            },
            {
                'name': 'Asian Clay & Rose Mask',
                'brand': 'Aurora Beauty',
                'category': 'Mask',
                'description': 'Purifying clay mask with rose extract.',
                'price': 27.99,
                'stock': 30,
                'suitable_for': 'Acne, Wrinkles, Oily Skin, Normal Skin',
                'targets': 'Deep Cleansing, Anti-aging',
                'when_to_apply': 'PM'
            },
            {
                'name': 'Intensive Skin Repair Sandal Lotion',
                'brand': 'Aurora Beauty',
                'category': 'Moisturizer',
                'description': 'Intensive repair lotion with sandalwood.',
                'price': 34.99,
                'stock': 40,
                'suitable_for': 'Acne, Eczema, Rosacea, Wrinkles, Dry Skin',
                'targets': 'Skin Repair, Moisturizing',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'Niacinamide & NEEM Toner',
                'brand': 'Aurora Beauty',
                'category': 'Toner',
                'description': 'Balancing toner with niacinamide and neem.',
                'price': 21.99,
                'stock': 45,
                'suitable_for': 'Acne, Rosacea, Oily Skin, Hyperpigmentation',
                'targets': 'Oil Control, Brightening',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'Charcoal Detox Soap',
                'brand': 'Aurora Beauty',
                'category': 'Cleanser',
                'description': 'Deep cleansing soap with activated charcoal.',
                'price': 16.99,
                'stock': 50,
                'suitable_for': 'Acne, Oily Skin',
                'targets': 'Deep Cleansing, Detoxifying',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'Lavender Soothing Lotion',
                'brand': 'Aurora Beauty',
                'category': 'Moisturizer',
                'description': 'Calming lotion with lavender extract.',
                'price': 29.99,
                'stock': 40,
                'suitable_for': 'Eczema, Rosacea, Dry Skin',
                'targets': 'Soothing, Moisturizing',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'Radiant Plump Serum',
                'brand': 'Aurora Beauty',
                'category': 'Serum',
                'description': 'Hydrating serum for plump, radiant skin.',
                'price': 39.99,
                'stock': 35,
                'suitable_for': 'Eczema, Rosacea, Wrinkles, Dry Skin, Hyperpigmentation',
                'targets': 'Hydration, Anti-aging',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'Radiant Rose Face Mist',
                'brand': 'Aurora Beauty',
                'category': 'Toner',
                'description': 'Refreshing rose mist for radiant skin.',
                'price': 23.99,
                'stock': 45,
                'suitable_for': 'Eczema, Rosacea, Dry Skin, Normal Skin',
                'targets': 'Hydration, Brightening',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'Radiant Plump Moisturizer with Glutathione',
                'brand': 'Aurora Beauty',
                'category': 'Moisturizer',
                'description': 'Advanced moisturizer with glutathione for radiant skin.',
                'price': 44.99,
                'stock': 30,
                'suitable_for': 'Eczema, Rosacea, Wrinkles, Dry Skin, Hyperpigmentation',
                'targets': 'Anti-aging, Brightening',
                'when_to_apply': 'AM/PM'
            },
            {
                'name': 'Sandal Glow Facial & Body Scrub',
                'brand': 'Aurora Beauty',
                'category': 'Scrub',
                'description': 'Exfoliating scrub with sandalwood for glowing skin.',
                'price': 26.99,
                'stock': 35,
                'suitable_for': 'Keratosis, Wrinkles, Dry Skin',
                'targets': 'Exfoliation, Brightening',
                'when_to_apply': 'PM'
            }
        ]

        for product_data in products:
            Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            self.stdout.write(f"Added/Updated product: {product_data['name']}") 