from django.urls import path
from . import views


urlpatterns = [
    # Customer routes
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("reservation/", views.reservation, name="reservation"),
    path("cart/", views.viewcart, name="cart"),
    path("api/create-order/", views.api_create_order, name="api_create_order"),
    path("api/get-tables/", views.api_get_tables, name="api_get_tables"),

    # Admin Panel routes
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-panel/dashboard/", views.admin_dashboard, name="admin_dashboard_alt"),
    path("admin-panel/orders/", views.admin_orders, name="admin_orders"),
    path("admin-panel/reservations/", views.admin_reservations, name="admin_reservations"),
    path("admin-panel/tables/", views.admin_tables, name="admin_tables"),
    path("admin-panel/advance-booking/", views.admin_advance_booking, name="admin_advance_booking"),
    path("admin-panel/menu/", views.admin_menu, name="admin_menu"),
    path("admin-panel/menu/add/", views.admin_addmenu, name="admin_addmenu"),
    path("admin-panel/menu/edit/<int:item_id>/", views.admin_editmenu, name="admin_editmenu"),
    path("admin-panel/menu/delete/<int:item_id>/", views.admin_deletemenu, name="admin_deletemenu"),
    path("admin-panel/customers/", views.admin_customers, name="admin_customers"),
    path("admin-panel/employees/", views.admin_employees, name="admin_employees"),
    path("admin-panel/inventory/", views.admin_inventory, name="admin_inventory"),
    path("admin-panel/payments/", views.admin_payments, name="admin_payments"),
    path("admin-panel/reports/", views.admin_reports, name="admin_reports"),
    path("admin-panel/profile/", views.admin_profile, name="admin_profile"),
    path("admin-panel/settings/", views.admin_settings, name="admin_settings"),

    # Admin Quick Actions APIs
    path("admin-panel/api/update-order-status/<int:order_id>/", views.admin_update_order_status, name="admin_update_order_status"),
    path("admin-panel/api/update-reservation-status/<int:res_id>/", views.admin_update_reservation_status, name="admin_update_reservation_status"),
    path("admin-panel/api/toggle-table/<int:table_id>/", views.admin_toggle_table, name="admin_toggle_table"),
    path("admin-panel/api/add-table/", views.admin_add_table, name="admin_add_table"),
]