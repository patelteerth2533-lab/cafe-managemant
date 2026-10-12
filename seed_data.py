"""
Bethak Cafe — Database Seeder
Run: python seed_data.py
Seeds: MenuCategory, MenuItem, CafeTable
"""

import os
import sys
import django

# ---- Django setup ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_project.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from cafe_app.models import MenuCategory, MenuItem, CafeTable

# ===========================
# MENU CATEGORIES
# ===========================
CATEGORIES = [
    {"name": "Coffee",          "slug": "coffee",       "icon": "bi-cup-hot",          "order": 1},
    {"name": "Fast Food",       "slug": "fastfood",     "icon": "bi-egg-fried",        "order": 2},
    {"name": "Desserts",        "slug": "desserts",     "icon": "bi-cake2",            "order": 3},
    {"name": "Beverages",       "slug": "beverages",    "icon": "bi-cup-straw",        "order": 4},
]

# ===========================
# MENU ITEMS
# ===========================
ITEMS = {
    "coffee": [
        ("Espresso",            89,  "image/menu coffee.png",    "Rich and bold single-shot espresso."),
        ("Cappuccino",          99,  "image/menu coffee.png",    "Espresso with steamed milk and thick foam."),
        ("Café Latte",          109, "image/menu coffee.png",    "Smooth espresso with velvety steamed milk."),
        ("Hazelnut Frappe",     149, "image/menu coffee.png",    "Cold blended coffee with hazelnut syrup."),
        ("Mocha",               119, "image/menu coffee.png",    "Chocolate and espresso blended perfectly."),
        ("Cold Brew",           139, "image/menu coffee.png",    "Slow-steeped cold brew coffee, served chilled."),
    ],
    "fastfood": [
        ("Veg Burger",          79,  "image/menu snacks.png",    "Crispy veggie patty with fresh veggies."),
        ("Chicken Burger",      99,  "image/menu snacks.png",    "Juicy grilled chicken with special sauce."),
        ("French Fries",        59,  "image/menu snacks.png",    "Golden crispy fries with dipping sauce."),
        ("Paneer Sandwich",     89,  "image/menu snacks.png",    "Grilled paneer with fresh mint chutney."),
        ("Crispy Nachos",       79,  "image/menu snacks.png",    "Crunchy nachos with salsa and cheese dip."),
        ("Spring Roll",         69,  "image/menu snacks.png",    "Crispy vegetable spring rolls, 3 pcs."),
    ],
    "desserts": [
        ("Chocolate Brownie",   99,  "image/menu dessert.png",   "Warm fudgy brownie with vanilla cream."),
        ("Gulab Jamun",         59,  "image/menu dessert.png",   "Soft milk solid dumplings in sugar syrup."),
        ("Cheesecake",          129, "image/menu dessert.png",   "Classic New York style baked cheesecake."),
        ("Mango Pannacotta",    119, "image/menu dessert.png",   "Silky smooth pannacotta with mango coulis."),
        ("Ice Cream Sundae",    89,  "image/menu dessert.png",   "Two scoops of ice cream with toppings."),
    ],
    "beverages": [
        ("Mango Shake",         99,  "image/menu shake&juice.png", "Fresh mango milkshake, thick and creamy."),
        ("Strawberry Smoothie", 109, "image/menu shake&juice.png", "Blended strawberries with yogurt and honey."),
        ("Lemon Iced Tea",      69,  "image/menu shake&juice.png", "Refreshing iced tea with fresh lemon."),
        ("Fresh Orange Juice",  79,  "image/menu shake&juice.png", "100% fresh squeezed orange juice."),
        ("Watermelon Juice",    59,  "image/menu shake&juice.png", "Chilled fresh watermelon juice."),
        ("Blue Lemonade",       89,  "image/menu shake&juice.png", "Blue curacao lemonade with mint."),
    ],
}

# ===========================
# CAFE TABLES
# ===========================
TABLES = [
    ("T-01", 2,  "Indoor",      "available"),
    ("T-02", 2,  "Indoor",      "available"),
    ("T-03", 4,  "Indoor",      "available"),
    ("T-04", 4,  "Indoor",      "available"),
    ("T-05", 4,  "Indoor",      "available"),
    ("T-06", 6,  "Family",      "available"),
    ("T-07", 6,  "Family",      "available"),
    ("T-08", 2,  "Window Seat", "available"),
    ("T-09", 2,  "Window Seat", "available"),
    ("T-10", 4,  "Outdoor",     "available"),
    ("T-11", 4,  "Outdoor",     "available"),
    ("T-12", 8,  "Family",      "available"),
]

# ===========================
# SEED LOGIC
# ===========================
def seed():
    print("=" * 50)
    print("  Bethak Cafe — Database Seeder")
    print("=" * 50)

    # 1. Categories
    cat_map = {}
    for c in CATEGORIES:
        obj, created = MenuCategory.objects.get_or_create(
            slug=c["slug"],
            defaults={"name": c["name"], "icon": c["icon"], "order": c["order"]}
        )
        cat_map[c["slug"]] = obj
        print(f"  {'[+]' if created else '[=]'} Category: {obj.name}")

    print()

    # 2. Menu Items
    for slug, items in ITEMS.items():
        cat = cat_map.get(slug)
        if not cat:
            continue
        for name, price, img, desc in items:
            obj, created = MenuItem.objects.get_or_create(
                name=name,
                category=cat,
                defaults={
                    "price": price,
                    "image_url": img,
                    "description": desc,
                    "stock": 50,
                    "is_available": True,
                }
            )
            print(f"  {'[+]' if created else '[=]'} Item: {obj.name} (Rs.{price})")

    print()

    # 3. Tables
    for number, seats, ttype, status in TABLES:
        obj, created = CafeTable.objects.get_or_create(
            table_number=number,
            defaults={"seats": seats, "table_type": ttype, "status": status}
        )
        print(f"  {'[+]' if created else '[=]'} Table: {obj.table_number} ({seats} seats, {ttype})")

    print()
    print("✅ Seeding complete!")
    print("=" * 50)

if __name__ == "__main__":
    seed()
