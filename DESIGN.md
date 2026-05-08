# Car Rental System — Design

## 1. Overview

A web platform where car owners list their vehicles and customers browse, book,
and pay for rentals. Built with Django 5 + MySQL + Bootstrap 5.

## 2. Roles

| Role       | Capabilities                                                         |
|------------|----------------------------------------------------------------------|
| Customer   | Browse cars, view details, book with date range, pay, leave reviews  |
| Car Owner  | List/edit/remove own cars, manage discounts, see incoming bookings   |
| Admin      | Full CRUD over all entities via Django admin                         |

A single Django `User` is extended with a `Profile.role` field
(`customer` or `owner`) chosen at registration. Admin uses `is_staff`.

## 3. Tech Stack

- **Backend:** Django 5.0, Python 3.13
- **Database:** MySQL 8 (via `mysqlclient`)
- **Frontend:** Server-rendered Django templates + Bootstrap 5 + minimal vanilla JS
- **Auth:** Django built-in auth (sessions)
- **Static/Media:** Local filesystem (dev); ready for S3 swap in prod

## 4. Data Model

```
User (django.contrib.auth)
 └─ Profile (1:1)              role, phone, city, street, zipcode

CarOwner ─ owns ─< Car >─ booked ─< Booking >─ by ─ Customer
                                      │
                                      ├─ uses ─ Discount (optional)
                                      ├─ paid by ─ Payment
                                      └─ rated by ─ Review
```

### Tables

**Profile** — extends `auth_user`
- `user` (OneToOne → User, PK)
- `role` (`customer` | `owner`)
- `phone`, `city`, `street`, `zipcode`

**Car**
- `id` (PK), `owner` (FK → User)
- `brand`, `model`, `year`
- `car_type` (`sedan` | `suv` | `hatchback` | `van` | `luxury`)
- `transmission` (`automatic` | `manual`)
- `seats`, `fuel` (`petrol` | `diesel` | `electric` | `hybrid`)
- `license_plate` (unique)
- `daily_rate` (decimal)
- `image` (URL string for simplicity in dev)
- `is_available` (bool)
- `created_at`

**Discount**
- `id` (PK), `owner` (FK → User)
- `code` (unique), `percentage` (1–100)
- `valid_from`, `valid_until`

**Booking**
- `id` (PK), `customer` (FK → User), `car` (FK → Car)
- `discount` (FK → Discount, nullable)
- `start_date`, `end_date`
- `total_cost` (decimal, computed at creation)
- `status` (`pending` | `confirmed` | `cancelled` | `completed`)
- `created_at`

**Payment**
- `id` (PK), `booking` (OneToOne → Booking)
- `amount`, `method` (`card` | `cash` | `gcash`), `paid_at`

**Review**
- `id` (PK), `booking` (OneToOne → Booking)
- `rating` (1–5), `comment`, `created_at`

## 5. URL Map

| Path                                | View                       | Auth        |
|-------------------------------------|----------------------------|-------------|
| `/`                                 | Home (hero + featured)     | public      |
| `/accounts/register/`               | Register (role chooser)    | public      |
| `/accounts/login/`                  | Login                      | public      |
| `/accounts/logout/`                 | Logout                     | any         |
| `/accounts/profile/`                | Edit profile               | any         |
| `/cars/`                            | Browse + filters           | public      |
| `/cars/<id>/`                       | Car detail + book widget   | public      |
| `/cars/owner/`                      | Owner: my cars             | owner       |
| `/cars/owner/new/`                  | Owner: add car             | owner       |
| `/cars/owner/<id>/edit/`            | Owner: edit car            | owner       |
| `/cars/owner/<id>/delete/`          | Owner: delete car          | owner       |
| `/cars/owner/discounts/`            | Owner: manage discounts    | owner       |
| `/bookings/new/<car_id>/`           | Create booking             | customer    |
| `/bookings/`                        | Customer: my bookings      | customer    |
| `/bookings/<id>/pay/`               | Pay for booking            | customer    |
| `/bookings/<id>/review/`            | Leave review               | customer    |
| `/bookings/owner/`                  | Owner: bookings on my cars | owner       |
| `/admin/`                           | Django admin               | staff       |

## 6. Key Flows

### 6.1 Customer booking flow
1. Browse `/cars/` → filter by type/brand/price.
2. Open car detail → pick start/end dates → submit booking form.
3. System validates date range, checks for overlap with existing
   `confirmed` bookings, applies discount code if present, computes total.
4. Booking created with status `pending`. Customer redirected to
   `/bookings/<id>/pay/`.
5. On payment, booking becomes `confirmed`.
6. After `end_date`, status auto-flips to `completed` (handled on read for
   simplicity in dev — a real deployment would use a cron/celery task).
7. Customer can leave one review per `completed` booking.

### 6.2 Owner listing flow
1. Register as Owner → owner dashboard.
2. Add car (brand, plate, daily rate, image URL).
3. Optionally create discount codes.
4. View incoming bookings, see status.

## 7. Trade-offs / Notes

- **Image upload vs URL:** dev uses image URLs (simpler — no media settings,
  no Pillow dep). For prod, swap to `ImageField` + S3.
- **Payment is mocked:** no real gateway. Recording a `Payment` row flips
  the booking to `confirmed`. Plug Stripe/PayPal later at this seam.
- **Overlap check on booking** is read-then-insert, not transactionally
  locked. Fine for low concurrency; for real load wrap in `select_for_update`
  inside `transaction.atomic`.
- **Auth:** Django's session auth, not JWT. Templates are server-rendered;
  no SPA. Trades frontend richness for simplicity and faster build.
- **Owners can only manage their own cars/discounts/bookings** — enforced
  in views via `owner=request.user` filters, not just URL guessing.

## 8. Folder Structure

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
