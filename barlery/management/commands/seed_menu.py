"""
Django management command to seed the database with sample menu items (beverages only).

Usage:
    python manage.py seed_menu
    python manage.py seed_menu --clear  # Clear existing menu items first
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from barlery.models import MenuItem


class Command(BaseCommand):
    help = 'Seeds the database with sample beverage menu items for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing menu items before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing menu items...')
            MenuItem.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ All menu items cleared'))

        self.stdout.write('Seeding menu items...')

        # Sample menu data with categories
        menu_data = [
            # BEERS - Craft & Specialty
            {
                'name': 'Chattanooga Brewing 1816 IPA',
                'category': 'beer',
                'abv': 6.5,
                'description': 'Local favorite with citrus and pine notes. Medium body with a crisp finish.',
                'price': 7.50,
            },
            {
                'name': 'Big River Grizzly Pale Ale',
                'category': 'beer',
                'abv': 5.8,
                'description': 'Tennessee pale ale with balanced malt and hop character.',
                'price': 7.00,
            },
            {
                'name': 'Naked River Hop Tart',
                'category': 'beer',
                'abv': 5.2,
                'description': 'Tart and hoppy blonde ale brewed with real fruit.',
                'price': 7.25,
            },
            {
                'name': 'Terminal Brewhouse 42 Stout',
                'category': 'beer',
                'abv': 6.8,
                'description': 'Rich chocolate and coffee notes with a smooth, creamy finish.',
                'price': 8.00,
            },
            {
                'name': "Blackhorse Pilsner",
                'category': 'beer',
                'abv': 5.0,
                'description': 'Crisp Czech-style pilsner with floral hops and light malt.',
                'price': 6.75,
            },
            {
                'name': 'Heaven & Ale Hazy IPA',
                'category': 'beer',
                'abv': 6.9,
                'description': 'Juicy New England style IPA with tropical fruit flavors.',
                'price': 8.50,
            },
            {
                'name': 'Southside Craft Amber Ale',
                'category': 'beer',
                'abv': 5.5,
                'description': 'Smooth amber ale with caramel notes and mild bitterness.',
                'price': 7.00,
            },
            {
                'name': 'OddStory Seasonal Sour',
                'category': 'beer',
                'abv': 5.4,
                'description': 'Rotating sour beer with unique fruit additions. Ask your server!',
                'price': 8.00,
            },
            
            # BEERS - Domestics & Imports
            {
                'name': 'Budweiser',
                'category': 'beer',
                'abv': 5.0,
                'description': 'Classic American lager.',
                'price': 4.50,
            },
            {
                'name': 'Coors Light',
                'category': 'beer',
                'abv': 4.2,
                'description': 'Light and refreshing.',
                'price': 4.50,
            },
            {
                'name': 'Miller Lite',
                'category': 'beer',
                'abv': 4.2,
                'description': 'Smooth, easy-drinking pilsner.',
                'price': 4.50,
            },
            {
                'name': 'Michelob Ultra',
                'category': 'beer',
                'abv': 4.2,
                'description': 'Light beer with only 95 calories.',
                'price': 5.00,
            },
            {
                'name': 'Corona Extra',
                'category': 'beer',
                'abv': 4.6,
                'description': 'Mexican pale lager, served with lime.',
                'price': 5.50,
            },
            {
                'name': 'Stella Artois',
                'category': 'beer',
                'abv': 5.0,
                'description': 'Belgian pilsner with a crisp, clean taste.',
                'price': 6.00,
            },
            {
                'name': 'Guinness Draught',
                'category': 'beer',
                'abv': 4.2,
                'description': 'Irish dry stout with creamy texture.',
                'price': 6.50,
            },
            {
                'name': 'Heineken',
                'category': 'beer',
                'abv': 5.0,
                'description': 'Dutch pale lager with a slightly bitter taste.',
                'price': 5.50,
            },
            {
                'name': 'Blue Moon Belgian White',
                'category': 'beer',
                'abv': 5.4,
                'description': 'Wheat beer with orange and coriander.',
                'price': 6.00,
            },

            # WINE
            {
                'name': 'House Red Wine',
                'category': 'wine',
                'abv': 13.5,
                'description': 'Smooth and fruity red blend. Glass or bottle.',
                'price': 8.00,
            },
            {
                'name': 'House White Wine',
                'category': 'wine',
                'abv': 12.5,
                'description': 'Crisp and refreshing white blend. Glass or bottle.',
                'price': 8.00,
            },
            {
                'name': 'Cabernet Sauvignon',
                'category': 'wine',
                'abv': 14.0,
                'description': 'Full-bodied red with dark fruit flavors.',
                'price': 10.00,
            },
            {
                'name': 'Chardonnay',
                'category': 'wine',
                'abv': 13.0,
                'description': 'Buttery white wine with oak notes.',
                'price': 9.00,
            },
            {
                'name': 'Pinot Grigio',
                'category': 'wine',
                'abv': 12.0,
                'description': 'Light and crisp Italian white.',
                'price': 9.00,
            },

            # SPIRITS
            {
                'name': 'Jack Daniels',
                'category': 'spirit',
                'abv': 40.0,
                'description': 'Tennessee whiskey. Served neat, on the rocks, or mixed.',
                'price': 8.00,
            },
            {
                'name': "Tito's Vodka",
                'category': 'spirit',
                'abv': 40.0,
                'description': 'Smooth American vodka.',
                'price': 7.00,
            },
            {
                'name': 'Captain Morgan Spiced Rum',
                'category': 'spirit',
                'abv': 35.0,
                'description': 'Caribbean rum with vanilla and spice.',
                'price': 7.00,
            },
            {
                'name': 'Patron Silver Tequila',
                'category': 'spirit',
                'abv': 40.0,
                'description': 'Premium 100% agave tequila.',
                'price': 10.00,
            },
            {
                'name': 'Tanqueray Gin',
                'category': 'spirit',
                'abv': 47.3,
                'description': 'Classic London dry gin.',
                'price': 8.00,
            },

            # FOOD
            {
                'name': 'Classic Hot Dog',
                'category': 'food',
                'abv': None,
                'description': 'All-beef hot dog on a toasted bun with your choice of toppings.',
                'price': 5.00,
            },
            {
                'name': 'Chili Cheese Dog',
                'category': 'food',
                'abv': None,
                'description': 'Hot dog topped with homemade chili and melted cheddar cheese.',
                'price': 7.00,
            },
            {
                'name': 'Chicago Dog',
                'category': 'food',
                'abv': None,
                'description': 'All-beef hot dog with mustard, relish, onions, tomatoes, pickle, peppers, and celery salt.',
                'price': 7.50,
            },
            {
                'name': 'BBQ Bacon Dog',
                'category': 'food',
                'abv': None,
                'description': 'Hot dog with crispy bacon, BBQ sauce, and fried onions.',
                'price': 7.50,
            },
            {
                'name': 'Veggie Dog',
                'category': 'food',
                'abv': None,
                'description': 'Plant-based hot dog with all the fixings.',
                'price': 6.00,
            },
            {
                'name': 'Pretzel Bites',
                'category': 'food',
                'abv': None,
                'description': 'Warm soft pretzel bites served with beer cheese dip.',
                'price': 6.00,
            },
            {
                'name': 'Loaded Nachos',
                'category': 'food',
                'abv': None,
                'description': 'Tortilla chips topped with cheese, jalapeños, sour cream, and salsa.',
                'price': 8.00,
            },
            {
                'name': 'Wings (6pc)',
                'category': 'food',
                'abv': None,
                'description': 'Crispy chicken wings tossed in your choice of sauce: Buffalo, BBQ, or Dry Rub.',
                'price': 9.00,
            },

            # NON-ALCOHOLIC
            {
                'name': 'Coca-Cola',
                'category': 'non-alcoholic',
                'abv': None,
                'description': 'Classic cola.',
                'price': 3.00,
            },
            {
                'name': 'Diet Coke',
                'category': 'non-alcoholic',
                'abv': None,
                'description': 'Zero calorie cola.',
                'price': 3.00,
            },
            {
                'name': 'Sprite',
                'category': 'non-alcoholic',
                'abv': None,
                'description': 'Lemon-lime soda.',
                'price': 3.00,
            },
            {
                'name': 'Ginger Ale',
                'category': 'non-alcoholic',
                'abv': None,
                'description': 'Refreshing ginger soda.',
                'price': 3.00,
            },
            {
                'name': 'Iced Tea',
                'category': 'non-alcoholic',
                'abv': None,
                'description': 'Freshly brewed, sweetened or unsweetened.',
                'price': 3.00,
            },
            {
                'name': 'Lemonade',
                'category': 'non-alcoholic',
                'abv': None,
                'description': 'House-made fresh lemonade.',
                'price': 3.50,
            },
            {
                'name': 'Coffee',
                'category': 'non-alcoholic',
                'abv': None,
                'description': 'Hot brewed coffee.',
                'price': 2.50,
            },
            {
                'name': 'Bottled Water',
                'category': 'non-alcoholic',
                'abv': None,
                'description': 'Still or sparkling.',
                'price': 2.00,
            },
            {
                'name': 'Red Bull Energy Drink',
                'category': 'non-alcoholic',
                'abv': None,
                'description': 'Original or sugar-free.',
                'price': 4.50,
            },
            {
                'name': 'Athletic Brewing NA IPA',
                'category': 'non-alcoholic',
                'abv': 0.0,
                'description': 'Non-alcoholic craft IPA with full hop flavor.',
                'price': 5.50,
            },
        ]

        # Create menu items
        created_count = 0
        for item_data in menu_data:
            item_data['last_updated'] = timezone.now()
            
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created: {item.name}')
            else:
                self.stdout.write(f'  - Skipped (already exists): {item.name}')

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully seeded {created_count} menu items!'))
        self.stdout.write(f'Total menu items in database: {MenuItem.objects.count()}')
        
        # Show breakdown by category
        from barlery.models import MenuItem as MI
        beer_count = MenuItem.objects.filter(category=MI.CATEGORY_BEER).count()
        wine_count = MenuItem.objects.filter(category=MI.CATEGORY_WINE).count()
        spirit_count = MenuItem.objects.filter(category=MI.CATEGORY_SPIRIT).count()
        food_count = MenuItem.objects.filter(category=MI.CATEGORY_FOOD).count()
        na_count = MenuItem.objects.filter(category=MI.CATEGORY_NON_ALCOHOLIC).count()
        
        self.stdout.write(f'\nBreakdown by Category:')
        self.stdout.write(f'  Beers: {beer_count}')
        self.stdout.write(f'  Wine: {wine_count}')
        self.stdout.write(f'  Spirits: {spirit_count}')
        self.stdout.write(f'  Food: {food_count}')
        self.stdout.write(f'  Non-Alcoholic Beverages: {na_count}')