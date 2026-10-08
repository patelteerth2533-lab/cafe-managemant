from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )
    fullname = models.CharField(max_length=150)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname} ({self.email})"


class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default="bi-cup-hot")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Menu Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.CharField(max_length=255, blank=True, default="")
    stock = models.PositiveIntegerField(default=50)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class CafeTable(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("booked", "Booked"),
        ("maintenance", "Under Maintenance"),
    )
    TABLE_TYPE_CHOICES = (
        ("Indoor", "Indoor"),
        ("Outdoor", "Outdoor"),
        ("Family", "Family"),
        ("Window Seat", "Window Seat"),
    )

    table_number = models.CharField(max_length=20, unique=True)
    seats = models.PositiveIntegerField(default=4)
    table_type = models.CharField(max_length=30, choices=TABLE_TYPE_CHOICES, default="Indoor")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    def __str__(self):
        return f"Table {self.table_number} ({self.seats} Seats - {self.status})"


class Reservation(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservations"
    )
    fullname = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    guests = models.PositiveIntegerField(default=2)
    date = models.DateField()
    time = models.TimeField()
    table_type = models.CharField(max_length=50, default="Indoor")
    table = models.ForeignKey(
        CafeTable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservations"
    )
    special_request = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reservation {self.id} - {self.fullname} ({self.status})"


class Order(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Preparing", "Preparing"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )
    PAYMENT_STATUS_CHOICES = (
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
        ("Refunded", "Refunded"),
    )

    order_id = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=15)
    table_number = models.CharField(max_length=20, blank=True, default="")
    guests = models.CharField(max_length=20, blank=True, default="")
    booking_date = models.DateField(null=True, blank=True)
    booking_time = models.TimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="Paid")
    payment_method = models.CharField(max_length=50, default="UPI")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name} (₹{self.total_amount})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    item_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"


class Payment(models.Model):
    METHOD_CHOICES = (
        ("UPI", "UPI"),
        ("Card", "Credit / Debit Card"),
        ("Cash", "Cash"),
        ("NetBanking", "Net Banking"),
    )
    STATUS_CHOICES = (
        ("Paid", "Paid"),
        ("Pending", "Pending"),
        ("Failed", "Failed"),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment_record"
    )
    transaction_id = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default="UPI")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Paid")
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-paid_at"]

    def __str__(self):
        return f"Payment {self.transaction_id} - ₹{self.amount} ({self.status})"