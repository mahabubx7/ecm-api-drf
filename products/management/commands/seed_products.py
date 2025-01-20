import csv
import os
import re
from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Seed products from CSV file'

    def handle(self, *args, **kwargs):
        try:
            csv_file_path = os.path.join(os.path.dirname(__file__), 'products__faisal_mamun.csv')
            with open(csv_file_path) as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Ensure category name is not empty
                    category_name = row['category']
                    if not category_name:
                        self.stdout.write(self.style.ERROR('Category name is empty, skipping row.'))
                        continue
                    
                    # Generate slug from category name
                    category_slug = category_name.lower().replace(' ', '-')
                    
                    # Get or create the category
                    category, _ = Category.objects.get_or_create(
                        name=category_name,
                        slug=category_slug
                    )
                    
                    # Extract stock value, handling cases like '30 dozen'
                    stock_value = row['Stock'] if row['Stock'] else '0'  # Default to '0' if empty
                    stock_numeric = re.findall(r'\d+', stock_value)  # Extract numeric part
                    stock = int(stock_numeric[0]) if stock_numeric else 0  # Convert to int, default to 0 if no number found

                    # Create the product
                    Product.objects.create(
                        name=row['Product Name'],
                        slug=row['Product Name'].lower().replace(' ', '-'),
                        description=row['Description'] if row['Description'] else '',
                        price=float(row['Price']) if row['Price'] else 0,  # Ensure price is a float
                        stock=stock,  # Use the extracted stock value
                        image=row['img link'] if row['img link'] else 'default.jpg',
                        category=category
                    )
            self.stdout.write(self.style.SUCCESS('Successfully seeded products'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))