import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_project.settings')
sys.path.insert(0, '.')
django.setup()

from django.contrib.auth.models import User
from cafe_app.models import MenuCategory, MenuItem, CafeTable, Reservation, Order, Customer

print('=== DATABASE STATUS ===')
u = User.objects.filter(is_superuser=True).first()
print(f'Superuser   : {u.username if u else "NONE"}')
print(f'Categories  : {MenuCategory.objects.count()}')
print(f'Menu Items  : {MenuItem.objects.count()}')
print(f'Tables      : {CafeTable.objects.count()}')
print(f'Orders      : {Order.objects.count()}')
print(f'Reservations: {Reservation.objects.count()}')
print(f'Customers   : {Customer.objects.count()}')
