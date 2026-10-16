from decimal import Decimal
from django.contrib.auth.models import User
from .models import MenuCategory, MenuItem, CafeTable

CATEGORIES = [
    {"name": "Coffee",      "slug": "coffee",    "icon": "bi-cup-hot",      "order": 1},
    {"name": "Fast Food",   "slug": "fastfood",  "icon": "bi-egg-fried",    "order": 2},
    {"name": "Desserts",    "slug": "desserts",  "icon": "bi-cake2",        "order": 3},
    {"name": "Beverages",   "slug": "beverages", "icon": "bi-cup-straw",    "order": 4},
]

ITEMS = {
    "coffee": [
        ("Espresso",        89,  "image/menu coffee.png",    "Rich and bold single-shot espresso with aromatic crema."),
        ("Cappuccino",      99,  "image/menu coffee.png",    "Espresso with velvety steamed milk and thick frothy foam."),
        ("Café Latte",      109, "image/menu coffee.png",    "Smooth roasted espresso balanced with creamy steamed milk."),
        ("Hazelnut Frappe", 149, "image/menu coffee.png",    "Chilled blended iced coffee infused with roasted hazelnut syrup."),
        ("Mocha",           119, "image/menu coffee.png",    "Rich Belgian chocolate and dark espresso blended to perfection."),
        ("Cold Brew",       139, "image/menu coffee.png",    "16-hour slow-steeped artisan cold brew coffee served chilled."),
    ],
    "fastfood": [
        ("Veg Burger",      79,  "image/menu snacks.png",    "Crispy spiced veggie patty with fresh lettuce and secret herb sauce."),
        ("Chicken Burger",  99,  "image/menu snacks.png",    "Juicy grilled chicken patty loaded with cheese and smoky mayo."),
        ("French Fries",    59,  "image/menu snacks.png",    "Golden crispy salted potato fries served with tangy dip."),
        ("Paneer Sandwich", 89,  "image/menu snacks.png",    "Grilled cottage cheese layered with mint chutney and melted cheese."),
        ("Crispy Nachos",   79,  "image/menu snacks.png",    "Crunchy corn tortilla chips with spicy Mexican salsa and cheese sauce."),
        ("Spring Roll",     69,  "image/menu snacks.png",    "Crispy fried vegetable spring rolls served with sweet chilli dip."),
    ],
    "desserts": [
        ("Chocolate Brownie", 99,  "image/menu dessert.png", "Warm fudgy walnut brownie served with hot chocolate fudge."),
        ("Gulab Jamun",       59,  "image/menu dessert.png", "Melt-in-mouth milk solid dumplings dipped in aromatic rose sugar syrup."),
        ("Cheesecake",        129, "image/menu dessert.png", "Classic New York style baked cheesecake with buttery graham crust."),
        ("Mango Pannacotta",  119, "image/menu dessert.png", "Silky Italian vanilla pannacotta topped with sweet Alphonso mango coulis."),
        ("Ice Cream Sundae",  89,  "image/menu dessert.png", "Two rich scoops of premium ice cream drizzled with syrups and nuts."),
    ],
    "beverages": [
        ("Mango Shake",       99,  "image/menu shake&juice.png", "Thick and creamy real Alphonso mango shake garnished with cream."),
        ("Strawberry Smoothie", 109, "image/menu shake&juice.png", "Blended farm strawberries with natural Greek yogurt and honey."),
        ("Lemon Iced Tea",    69,  "image/menu shake&juice.png", "Brisk chilled Ceylon tea infused with fresh squeezed lemon and mint."),
        ("Fresh Orange Juice", 79,  "image/menu shake&juice.png", "100% pure fresh Valencia orange juice squeezed to order."),
        ("Watermelon Juice",  59,  "image/menu shake&juice.png", "Hydrating chilled fresh watermelon cooler with fresh mint leaves."),
        ("Blue Lemonade",     89,  "image/menu shake&juice.png", "Zesty blue curacao lemonade with sparkling soda and ice."),
    ],
}

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


def ensure_seed_data(quiet=False):
    """
    Ensures default admin user, menu categories, menu items, and tables exist.
    Safe to run multiple times (idempotent).
    """
    # 1. Admin Superuser
    admin, created = User.objects.get_or_create(username="admin")
    admin.email = "admin@bethakcafe.com"
    admin.first_name = "Bethak"
    admin.last_name = "Admin"
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password("admin123")
    admin.save()
    if not quiet:
        print(f"  {'[+] Created' if created else '[=] Verified'} Superuser 'admin' (Password: admin123)")

    # Also ensure user 'teerth' has admin permissions & admin123 password
    for uname in ["teerth", "Teerth@1234"]:
        t_user = User.objects.filter(username__iexact=uname).first()
        if t_user:
            t_user.is_staff = True
            t_user.is_superuser = True
            t_user.set_password("admin123")
            t_user.save()
            if not quiet:
                print(f"  [=] Synchronized Admin '{uname}' (Password: admin123)")

    # 2. Categories
    cat_map = {}
    for c in CATEGORIES:
        cat_obj, c_created = MenuCategory.objects.get_or_create(
            slug=c["slug"],
            defaults={"name": c["name"], "icon": c["icon"], "order": c["order"]}
        )
        cat_map[c["slug"]] = cat_obj
        if not quiet and c_created:
            print(f"  [+] Created Category '{cat_obj.name}'")

    # 3. Menu Items
    for slug, items in ITEMS.items():
        cat = cat_map.get(slug)
        if not cat:
            continue
        for name, price, img, desc in items:
            item_obj, i_created = MenuItem.objects.get_or_create(
                name=name,
                category=cat,
                defaults={
                    "price": Decimal(str(price)),
                    "image_url": img,
                    "description": desc,
                    "stock": 50,
                    "is_available": True,
                }
            )
            # Update image if empty
            if not item_obj.image_url:
                item_obj.image_url = img
                item_obj.save()
            if not quiet and i_created:
                print(f"  [+] Created Item '{item_obj.name}' (Rs. {price})")

    # 4. Tables
    for number, seats, ttype, status in TABLES:
        t_obj, t_created = CafeTable.objects.get_or_create(
            table_number=number,
            defaults={"seats": seats, "table_type": ttype, "status": status}
        )
        if not quiet and t_created:
            print(f"  [+] Created Table '{t_obj.table_number}'")
