# Car Rental

A role-based car rental web platform built with Django 5 and MySQL. Car owners list their vehicles; customers browse, book, pay, and review.

See [DESIGN.md](DESIGN.md) for the full design document (data model, URL map, flows, trade-offs).

## Features

- **Customers** — browse cars with filters, book by date range, pay, and leave reviews on completed rentals.
- **Car owners** — list/edit/remove their own cars, create discount codes, and view incoming bookings.
- **Admin** — full CRUD over every entity via the Django admin.
- Single Django `User` extended with a `Profile.role` (`customer` or `owner`) chosen at registration.

## Tech Stack

- Backend: Django 5.0, Python 3.13
- Database: MySQL 8 (`mysqlclient`)
- Frontend: Server-rendered Django templates + Bootstrap 5
- Auth: Django built-in session auth

## Project Layout

```
carRental/
  manage.py
  carRental/        project: settings, urls, wsgi
  accounts/         Profile, register/login/profile views
  cars/             Car CRUD, browse, detail, discounts
  bookings/         Booking, Payment, Review
  templates/        base.html + per-app templates
  static/css/       site stylesheet
```

## Setup

### 1. Prerequisites

- Python 3.13
- MySQL 8 running locally
- `pip` / `venv`

### 2. Clone and install

```powershell
git clone <repo-url>
cd Car_Rental
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "Django>=5.0,<6.0" mysqlclient
```

### 3. Configure the database

Create a MySQL database named `carrental` (the credentials in [carRental/carRental/settings.py](carRental/carRental/settings.py) default to user `root` / password `root` on `127.0.0.1:3306` — edit them or match locally):

```sql
CREATE DATABASE carrental CHARACTER SET utf8mb4;
```

### 4. Migrate and run

```powershell
cd carRental
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Key URLs

| Path                         | Purpose                            |
|------------------------------|------------------------------------|
| `/`                          | Home                               |
| `/accounts/register/`        | Register as customer or owner      |
| `/cars/`                     | Browse cars with filters           |
| `/cars/<id>/`                | Car detail + booking widget        |
| `/cars/owner/`               | Owner dashboard (their cars)       |
| `/bookings/`                 | Customer: my bookings              |
| `/bookings/owner/`           | Owner: bookings on their cars      |
| `/admin/`                    | Django admin                       |

Full URL map in [DESIGN.md](DESIGN.md#5-url-map).

## Notes

- `DEBUG = True` and a hardcoded `SECRET_KEY` are checked in for dev convenience — change both before deploying.
- Payment is mocked: recording a `Payment` row flips the booking to `confirmed`. Replace at that seam to plug in Stripe/PayPal.
- Car images are stored as URL strings in dev; swap to `ImageField` + S3 for production.
