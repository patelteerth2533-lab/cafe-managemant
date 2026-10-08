from django.contrib import admin
from .models import (
    Customer,
    MenuCategory,
    MenuItem,
    CafeTable,
    Reservation,
    Order,
    OrderItem,
    Payment,
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "mobile", "created_at")
    search_fields = ("fullname", "email", "mobile")


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")


@admin.register(CafeTable)
class CafeTableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "seats", "table_type", "status")
    list_filter = ("status", "table_type")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("fullname", "mobile", "guests", "date", "time", "table", "status")
    list_filter = ("status", "date")
    search_fields = ("fullname", "email", "mobile")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer_name", "customer_phone", "total_amount", "status", "payment_status", "created_at")
    list_filter = ("status", "payment_status", "created_at")
    search_fields = ("order_id", "customer_name", "customer_phone")
    inlines = [OrderItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "order", "amount", "payment_method", "status", "paid_at")
    list_filter = ("payment_method", "status", "paid_at")
    search_fields = ("transaction_id", "order__order_id")
