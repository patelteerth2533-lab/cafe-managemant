from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Customer


# =========================
# HOME
# =========================

def home(request):
    return render(request, "customer/index.html")


# =========================
# MENU
# =========================

def menu(request):
    return render(request, "customer/menu.html")


# =========================
# LOGIN
# =========================

def login_page(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("home")

    # Login form submit
    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        role = request.POST.get("role", "customer")

        # Debug information
        print("================================")
        print("LOGIN POST")
        print("Email:", email)
        print("Role:", role)
        print("================================")

        # Empty fields
        if not email or not password:

            messages.error(
                request,
                "Please enter email and password."
            )

            return render(
                request,
                "customer/login.html"
            )

        # Find user by email
        try:

            user = User.objects.get(
                email__iexact=email
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "Invalid email or password."
            )

            return render(
                request,
                "customer/login.html"
            )

        # Check password
        authenticated_user = authenticate(
            request,
            username=user.username,
            password=password
        )

        # Wrong password
        if authenticated_user is None:

            messages.error(
                request,
                "Invalid email or password."
            )

            return render(
                request,
                "customer/login.html"
            )

        # =========================
        # CUSTOMER LOGIN
        # =========================

        if role == "customer":

            # Check Customer profile
            if not hasattr(
                user,
                "customer_profile"
            ):

                messages.error(
                    request,
                    "Customer account not found."
                )

                return render(
                    request,
                    "customer/login.html"
                )

            # Login
            login(
                request,
                authenticated_user
            )

            messages.success(
                request,
                "Login successful!"
            )

            # Customer goes to HOME
            return redirect("home")


        # =========================
        # ADMIN LOGIN
        # =========================

        elif role == "admin":

            # Check admin permission
            if not user.is_staff:

                messages.error(
                    request,
                    "You are not authorized as admin."
                )

                return render(
                    request,
                    "customer/login.html"
                )

            # Admin login
            login(
                request,
                authenticated_user
            )

            messages.success(
                request,
                "Admin login successful!"
            )

            # Django admin panel
            return redirect("/admin/")


        # =========================
        # INVALID ROLE
        # =========================

        else:

            messages.error(
                request,
                "Invalid login role."
            )

            return render(
                request,
                "customer/login.html"
            )

    # Normal GET request
    return render(
        request,
        "customer/login.html"
    )


# =========================
# REGISTER
# =========================

def register(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("home")

    # Registration form submit
    if request.method == "POST":

        fullname = request.POST.get(
            "fullname",
            ""
        ).strip()

        mobile = request.POST.get(
            "mobile",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        # =========================
        # REQUIRED FIELDS
        # =========================

        if (
            not fullname
            or not mobile
            or not email
            or not password
            or not confirm_password
        ):

            messages.error(
                request,
                "Please fill all required fields."
            )

            return render(
                request,
                "customer/register.html"
            )

        # =========================
        # MOBILE VALIDATION
        # =========================

        if not mobile.isdigit() or len(mobile) != 10:

            messages.error(
                request,
                "Please enter a valid 10-digit mobile number."
            )

            return render(
                request,
                "customer/register.html"
            )

        # =========================
        # PASSWORD MATCH
        # =========================

        if password != confirm_password:

            messages.error(
                request,
                "Password and Confirm Password do not match."
            )

            return render(
                request,
                "customer/register.html"
            )

        # =========================
        # PASSWORD LENGTH
        # =========================

        if len(password) < 8:

            messages.error(
                request,
                "Password must contain at least 8 characters."
            )

            return render(
                request,
                "customer/register.html"
            )

        # =========================
        # EMAIL ALREADY EXISTS
        # =========================

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "This email is already registered."
            )

            return render(
                request,
                "customer/register.html"
            )

        # =========================
        # CREATE DJANGO USER
        # =========================

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # =========================
        # CREATE CUSTOMER PROFILE
        # =========================

        Customer.objects.create(
            user=user,
            fullname=fullname,
            mobile=mobile,
            email=email
        )

        # =========================
        # SUCCESS
        # =========================

        messages.success(
            request,
            "Registration successful! Please login."
        )

        return redirect("login")

    # Normal GET request
    return render(
        request,
        "customer/register.html"
    )


# =========================
# RESERVATION
# =========================

def reservation(request):
    return render(
        request,
        "customer/reservation.html"
    )


# =========================
# CART
# =========================

def viewcart(request):
    return render(
        request,
        "customer/viewcart.html"
    )


# =========================
# LOGOUT
# =========================

def logout_user(request):

    logout(request)

    return redirect("home")