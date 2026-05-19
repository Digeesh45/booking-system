### booking

book

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app booking
# Mini Booking System - Frappe App

## Overview

This is a custom Frappe application for managing service bookings.

The system supports:

- Service Providers (Doctor/Nurse)
- Service Categories
- Service Bookings
- Auto Provider Assignment
- Distance-based Pricing
- Booking Status Workflow
- Provider Performance Report
- REST APIs

---

# Features

## 1. Service Provider Management

Manage doctors and nurses with:

- Name
- Type
- Rating
- Availability
- Location
- Contact Details

---

## 2. Service Booking Management

Customers can:

- Create bookings
- Track booking status
- Get assigned providers automatically

---

## 3. Auto Provider Assignment

Nearest available provider is automatically assigned based on:

- Distance
- Provider Rating

---

## 4. Dynamic Price Calculation

Price is calculated using:

Base Price + (Distance × Price Per KM)

---

## 5. Workflow Management

Booking statuses:

- Draft
- Pending
- Accepted
- Completed
- Cancelled

---

# DocTypes

## Service Provider

Fields:

- Provider Name
- Provider Type
- Email
- Phone
- Location
- Latitude
- Longitude
- Rating
- Availability Status
- Total Bookings

---

## Service Category

Fields:

- Category Name
- Base Price
- Price Per KM

---

## Service Booking

Fields:

- Customer Name
- Customer Phone
- Service Category
- Assigned Provider
- Latitude
- Longitude
- Distance
- Price
- Status
- Booking Time

---

# API Endpoints

Base URL:

```bash
http://127.0.0.1:8003/api/method/booking.api.booking```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/booking
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
