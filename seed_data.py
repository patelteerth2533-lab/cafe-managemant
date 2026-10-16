"""
Bethak Cafe — Database Seeder
Run: python seed_data.py
Seeds: Admin user, MenuCategory, MenuItem, CafeTable
"""

import os
import sys
import django

# ---- Django setup ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_project.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from cafe_app.seed_helper import ensure_seed_data


def seed():
    print("=" * 55)
    print("  Bethak Cafe - Database Seeder & Admin Provisioning")
    print("=" * 55)
    ensure_seed_data(quiet=False)
    print("=" * 55)
    print("  [OK] All categories, items, tables, and admin user verified!")
    print("       Admin Username : admin")
    print("       Admin Password : admin123")
    print("=" * 55)


if __name__ == "__main__":
    seed()
