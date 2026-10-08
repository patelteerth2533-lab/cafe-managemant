# Cafe Management System

A web-based Cafe Management System built using **Django** and **MySQL**, designed to handle customer orders, table reservations, and administrative operations.

## Features

- **Customer Portal**:
  - Browse Cafe Menu with categories and pricing
  - Cart and Order placement
  - Online Table Reservation
  - User Authentication (Registration / Login)

- **Admin Portal**:
  - Admin Dashboard & Analytics
  - Table & Seating Management
  - Order & Payment Tracking
  - Menu Management (Add / Edit / Remove items)
  - Inventory & Employee Management
  - Advance Bookings & Reports

## Tech Stack

- **Backend**: Python, Django
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Static Assets**: Custom CSS and JS animations

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL Server (e.g., XAMPP, WampServer, or MySQL Server)
- Git

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd Cafe_management
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**:
   - Ensure MySQL is running on `127.0.0.1:3306`.
   - Create the database:
     ```sql
     CREATE DATABASE cafe_management;
     ```
   - If required, adjust database credentials in `cafe_project/settings.py`.

5. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser (Optional, for admin panel access)**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open your browser and visit `http://127.0.0.1:8000/`.
