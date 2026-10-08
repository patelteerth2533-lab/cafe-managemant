import json
import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count

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


def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# =========================
# CUSTOMER VIEWS
# =========================

def home(request):
    featured_categories = MenuCategory.objects.all().prefetch_related("items")[:4]
    customer_profile = None
    if request.user.is_authenticated and hasattr(request.user, "customer_profile"):
        customer_profile = request.user.customer_profile
    return render(request, "customer/index.html", {
        "categories": featured_categories,
        "customer": customer_profile,
    })


def menu(request):
    categories = MenuCategory.objects.all().prefetch_related("items")
    customer_profile = None
    if request.user.is_authenticated and hasattr(request.user, "customer_profile"):
        customer_profile = request.user.customer_profile
    return render(request, "customer/menu.html", {
        "categories": categories,
        "customer": customer_profile,
    })


def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_dashboard")
        return redirect("home")

    if request.method == "POST":
        email_or_user = request.POST.get("email", "").strip()
        secret = request.POST.get("password", "")
        chosen_role = request.POST.get("role", "customer")

        if not email_or_user or not secret:
            messages.error(request, "Please enter your username/email and password.")
            return render(request, "customer/login.html")

        # Try to find user by email or by username
        user_obj = None
        if "@" in email_or_user:
            user_obj = User.objects.filter(email__iexact=email_or_user).first()
        if not user_obj:
            user_obj = User.objects.filter(username__iexact=email_or_user).first()

        username_to_auth = user_obj.username if user_obj else email_or_user
        authenticated_user = authenticate(request, username=username_to_auth, password=secret)

        if authenticated_user is None:
            messages.error(request, "Invalid username/email or password.")
            return render(request, "customer/login.html")

        if chosen_role == "customer":
            login(request, authenticated_user)
            messages.success(request, f"Welcome back, {authenticated_user.first_name or authenticated_user.username}!")
            return redirect("home")

        elif chosen_role == "admin":
            if not (authenticated_user.is_staff or authenticated_user.is_superuser):
                messages.error(request, "You are not authorized as admin.")
                return render(request, "customer/login.html")

            login(request, authenticated_user)
            messages.success(request, "Admin login successful!")
            return redirect("admin_dashboard")

        else:
            messages.error(request, "Invalid login role selected.")
            return render(request, "customer/login.html")

    return render(request, "customer/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        full_name = request.POST.get("fullname", "").strip()
        mobile_number = request.POST.get("mobile", "").strip()
        email = request.POST.get("email", "").strip().lower()
        secret = request.POST.get("password", "")
        confirm_secret = request.POST.get("confirm_password", "")

        if not full_name or not mobile_number or not email or not secret or not confirm_secret:
            messages.error(request, "Please fill all required fields.")
            return render(request, "customer/register.html")

        if not mobile_number.isdigit() or len(mobile_number) < 10:
            messages.error(request, "Please enter a valid 10-digit mobile number.")
            return render(request, "customer/register.html")

        if secret != confirm_secret:
            messages.error(request, "Password and Confirm Password do not match.")
            return render(request, "customer/register.html")

        if len(secret) < 6:
            messages.error(request, "Password must contain at least 6 characters.")
            return render(request, "customer/register.html")

        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            messages.error(request, "This email is already registered. Please login.")
            return render(request, "customer/register.html")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=secret,
            first_name=full_name,
        )

        Customer.objects.create(
            user=user,
            fullname=full_name,
            mobile=mobile_number,
            email=email,
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "customer/register.html")


def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


def reservation(request):
    tables = CafeTable.objects.all().order_by("table_number")
    customer_profile = None
    if request.user.is_authenticated and hasattr(request.user, "customer_profile"):
        customer_profile = request.user.customer_profile

    if request.method == "POST":
        fullname = request.POST.get("fullname", "").strip()
        email = request.POST.get("email", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        guests = request.POST.get("guests", "2")
        date = request.POST.get("date", "")
        time = request.POST.get("time", "")
        table_type = request.POST.get("table_type", "Indoor")
        table_no = request.POST.get("selected_table", "").strip()
        message = request.POST.get("message", "").strip()

        # Extract digit from guest string (e.g. "4 Guests" -> 4)
        guests_count = 2
        for ch in guests.split():
            if ch.isdigit():
                guests_count = int(ch)
                break

        table_obj = None
        if table_no and table_no != "None":
            table_obj = CafeTable.objects.filter(table_number__iexact=table_no).first()

        res = Reservation.objects.create(
            customer=customer_profile,
            fullname=fullname or (customer_profile.fullname if customer_profile else "Guest"),
            email=email or (customer_profile.email if customer_profile else ""),
            mobile=mobile or (customer_profile.mobile if customer_profile else ""),
            guests=guests_count,
            date=date,
            time=time,
            table_type=table_type,
            table=table_obj,
            special_request=message,
            status="Pending"
        )
        if table_obj:
            table_obj.status = "booked"
            table_obj.save()

        messages.success(request, f"Table reserved successfully! Your reservation ID is #{res.id}.")
        return redirect("reservation")

    return render(request, "customer/reservation.html", {
        "tables": tables,
        "customer": customer_profile,
    })


def viewcart(request):
    tables = CafeTable.objects.filter(status="available")
    customer_profile = None
    if request.user.is_authenticated and hasattr(request.user, "customer_profile"):
        customer_profile = request.user.customer_profile
    return render(request, "customer/viewcart.html", {
        "tables": tables,
        "customer": customer_profile,
    })


def api_get_tables(request):
    tables = CafeTable.objects.all().order_by("table_number")
    data = [
        {
            "id": t.id,
            "number": t.table_number,
            "seats": t.seats,
            "type": t.table_type,
            "status": t.status,
        }
        for t in tables
    ]
    return JsonResponse({"tables": data})


@csrf_exempt
def api_create_order(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()
        table = data.get("table", "")
        guests = str(data.get("guests", ""))
        date = data.get("date", "")
        time = data.get("time", "")
        items = data.get("items", [])
        payment_method = data.get("payment_method", "UPI")

        if not name or not phone or not items:
            return JsonResponse({"status": "error", "message": "Customer name, phone, and items are required."}, status=400)

        order_id = "ORD" + uuid.uuid4().hex[:6].upper()
        total_amount = Decimal("0.00")

        customer_profile = None
        if request.user.is_authenticated and hasattr(request.user, "customer_profile"):
            customer_profile = request.user.customer_profile

        new_order = Order.objects.create(
            order_id=order_id,
            customer=customer_profile,
            customer_name=name,
            customer_phone=phone,
            table_number=table,
            guests=guests,
            booking_date=date if date else None,
            booking_time=time if time else None,
            total_amount=Decimal("0.00"),
            status="Pending",
            payment_status="Paid",
            payment_method=payment_method,
        )

        for it in items:
            it_name = it.get("name", "Food Item")
            it_price = Decimal(str(it.get("price", 0)))
            it_qty = int(it.get("qty", 1))
            line_total = it_price * it_qty
            total_amount += line_total

            OrderItem.objects.create(
                order=new_order,
                item_name=it_name,
                price=it_price,
                quantity=it_qty,
            )

        new_order.total_amount = total_amount
        new_order.save()

        # Create payment record
        Payment.objects.create(
            order=new_order,
            transaction_id="TXN" + uuid.uuid4().hex[:8].upper(),
            amount=total_amount,
            payment_method=payment_method,
            status="Paid",
        )

        return JsonResponse({
            "status": "success",
            "order_id": new_order.order_id,
            "total": float(new_order.total_amount),
            "created_at": new_order.created_at.strftime("%Y-%m-%d %H:%M"),
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


# =========================
# ADMIN PANEL VIEWS
# =========================

def admin_check_decorator(view_func):
    return user_passes_test(is_admin_user, login_url="login")(view_func)


@admin_check_decorator
def admin_dashboard(request):
    total_orders = Order.objects.count()
    revenue = Payment.objects.filter(status="Paid").aggregate(Sum("amount"))["amount__sum"] or 0
    reservations_count = Reservation.objects.count()
    customers_count = Customer.objects.count()
    recent_orders = Order.objects.all().prefetch_related("items")[:6]

    return render(request, "admin/admin_dashboard.html", {
        "total_orders": total_orders,
        "revenue": revenue,
        "reservations_count": reservations_count,
        "customers_count": customers_count,
        "recent_orders": recent_orders,
    })


@admin_check_decorator
def admin_orders(request):
    orders = Order.objects.all().prefetch_related("items")
    status_filter = request.GET.get("status")
    search_q = request.GET.get("q")

    if status_filter and status_filter != "All Status":
        orders = orders.filter(status=status_filter)
    if search_q:
        orders = orders.filter(order_id__icontains=search_q) | orders.filter(customer_name__icontains=search_q)

    total_count = Order.objects.count()
    pending_count = Order.objects.filter(status="Pending").count()
    preparing_count = Order.objects.filter(status="Preparing").count()
    completed_count = Order.objects.filter(status="Completed").count()

    return render(request, "admin/admin_order.html", {
        "orders": orders,
        "total_count": total_count,
        "pending_count": pending_count,
        "preparing_count": preparing_count,
        "completed_count": completed_count,
    })


@admin_check_decorator
def admin_reservations(request):
    reservations = Reservation.objects.all()
    search_q = request.GET.get("q")
    date_filter = request.GET.get("date")

    if search_q:
        reservations = reservations.filter(fullname__icontains=search_q)
    if date_filter:
        reservations = reservations.filter(date=date_filter)

    total = Reservation.objects.count()
    pending = Reservation.objects.filter(status="Pending").count()
    approved = Reservation.objects.filter(status="Approved").count()
    completed = Reservation.objects.filter(status="Completed").count()

    return render(request, "admin/admin_reservation.html", {
        "reservations": reservations,
        "total": total,
        "pending": pending,
        "approved": approved,
        "completed": completed,
    })


@admin_check_decorator
def admin_tables(request):
    tables = CafeTable.objects.all().order_by("table_number")
    total_tables = tables.count()
    available_tables = tables.filter(status="available").count()
    booked_tables = tables.filter(status="booked").count()

    return render(request, "admin/admin_table_manage.html", {
        "tables": tables,
        "total_tables": total_tables,
        "available_tables": available_tables,
        "booked_tables": booked_tables,
    })


@admin_check_decorator
def admin_advance_booking(request):
    bookings = Order.objects.filter(booking_date__isnull=False).prefetch_related("items")
    if not bookings.exists():
        bookings = Order.objects.all().prefetch_related("items")

    total = bookings.count()
    pending = bookings.filter(status="Pending").count()
    confirmed = bookings.filter(status__in=["Preparing", "Completed"]).count()
    amount = bookings.aggregate(Sum("total_amount"))["total_amount__sum"] or 0

    return render(request, "admin/admin_advance_booking.html", {
        "bookings": bookings,
        "total": total,
        "pending": pending,
        "confirmed": confirmed,
        "amount": amount,
    })


@admin_check_decorator
def admin_menu(request):
    items = MenuItem.objects.all().select_related("category")
    categories = MenuCategory.objects.all()
    cat_filter = request.GET.get("category")
    search_q = request.GET.get("q")

    if cat_filter and cat_filter != "All Categories":
        items = items.filter(category__name__iexact=cat_filter)
    if search_q:
        items = items.filter(name__icontains=search_q)

    return render(request, "admin/admin_menu.html", {
        "items": items,
        "categories": categories,
    })


@admin_check_decorator
def admin_addmenu(request):
    categories = MenuCategory.objects.all()
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        cat_id = request.POST.get("category")
        price = request.POST.get("price", "0")
        stock = request.POST.get("stock", "50")
        desc = request.POST.get("description", "")
        status = request.POST.get("status", "Available")
        img = request.POST.get("image_url", "image/menu coffee.png")

        category = MenuCategory.objects.filter(id=cat_id).first()
        if category and name:
            MenuItem.objects.create(
                category=category,
                name=name,
                price=Decimal(price),
                stock=int(stock) if stock else 0,
                description=desc,
                is_available=(status == "Available"),
                image_url=img,
            )
            messages.success(request, f"Food item '{name}' added successfully!")
            return redirect("admin_menu")

    return render(request, "admin/admin_addmenu.html", {"categories": categories})


@admin_check_decorator
def admin_editmenu(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    categories = MenuCategory.objects.all()

    if request.method == "POST":
        item.name = request.POST.get("name", item.name).strip()
        cat_id = request.POST.get("category")
        if cat_id:
            cat = MenuCategory.objects.filter(id=cat_id).first()
            if cat:
                item.category = cat
        item.price = Decimal(request.POST.get("price", str(item.price)))
        stock_val = request.POST.get("stock")
        if stock_val:
            item.stock = int(stock_val)
        item.description = request.POST.get("description", item.description)
        item.is_available = (request.POST.get("status") == "Available")
        item.save()
        messages.success(request, f"'{item.name}' updated successfully!")
        return redirect("admin_menu")

    return render(request, "admin/admin_editmenu.html", {
        "item": item,
        "categories": categories,
    })


@admin_check_decorator
def admin_deletemenu(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    name = item.name
    item.delete()
    messages.success(request, f"'{name}' deleted successfully.")
    return redirect("admin_menu")


@admin_check_decorator
def admin_customers(request):
    customers = Customer.objects.all().select_related("user")
    total = customers.count()
    active = customers.filter(user__is_active=True).count()
    new_users = customers.order_by("-created_at")[:10].count()
    return render(request, "admin/admin_customer.html", {
        "customers": customers,
        "total": total,
        "active": active,
        "new_users": new_users,
    })


@admin_check_decorator
def admin_employees(request):
    return render(request, "admin/admin_employe.html")


@admin_check_decorator
def admin_inventory(request):
    items = MenuItem.objects.all()
    total_items = items.count()
    low_stock = items.filter(stock__lte=15).count()
    out_of_stock = items.filter(stock=0).count()
    return render(request, "admin/admin_inventory.html", {
        "items": items,
        "total_items": total_items,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
    })


@admin_check_decorator
def admin_payments(request):
    payments = Payment.objects.all().select_related("order")
    total_rev = payments.filter(status="Paid").aggregate(Sum("amount"))["amount__sum"] or 0
    paid_count = payments.filter(status="Paid").count()
    pending_count = payments.filter(status="Pending").count()

    return render(request, "admin/admin_payments.html", {
        "payments": payments,
        "total_rev": total_rev,
        "paid_count": paid_count,
        "pending_count": pending_count,
    })


@admin_check_decorator
def admin_reports(request):
    total_sales = Payment.objects.filter(status="Paid").aggregate(Sum("amount"))["amount__sum"] or 0
    orders_count = Order.objects.count()
    customers_count = Customer.objects.count()
    top_items = MenuItem.objects.all().order_by("-stock")[:5]

    return render(request, "admin/admin_reports.html", {
        "total_sales": total_sales,
        "orders_count": orders_count,
        "customers_count": customers_count,
        "top_items": top_items,
    })


@admin_check_decorator
def admin_profile(request):
    return render(request, "admin/admin_profile.html", {"user": request.user})


@admin_check_decorator
def admin_settings(request):
    return render(request, "admin/admin_seating.html")


# Quick Action Handlers for Admin
@csrf_exempt
@admin_check_decorator
def admin_update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get("status") or request.GET.get("status", "Completed")
    order.status = new_status
    order.save()
    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("ajax"):
        return JsonResponse({"status": "success", "new_status": new_status})
    return redirect("admin_orders")


@csrf_exempt
@admin_check_decorator
def admin_update_reservation_status(request, res_id):
    res = get_object_or_404(Reservation, id=res_id)
    new_status = request.POST.get("status") or request.GET.get("status", "Approved")
    res.status = new_status
    res.save()
    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("ajax"):
        return JsonResponse({"status": "success", "new_status": new_status})
    return redirect("admin_reservations")


@csrf_exempt
@admin_check_decorator
def admin_toggle_table(request, table_id):
    table = get_object_or_404(CafeTable, id=table_id)
    table.status = "booked" if table.status == "available" else "available"
    table.save()
    return JsonResponse({"status": "success", "table_id": table.id, "new_status": table.status})


@csrf_exempt
@admin_check_decorator
def admin_add_table(request):
    if request.method == "POST":
        table_number = request.POST.get("table_number")
        seats = request.POST.get("seats", 4)
        table_type = request.POST.get("table_type", "Indoor")
        status = request.POST.get("status", "available")
        if table_number:
            CafeTable.objects.create(
                table_number=table_number,
                seats=int(seats),
                table_type=table_type,
                status=status
            )
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

