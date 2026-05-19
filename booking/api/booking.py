import frappe
from frappe import _
from frappe.utils import now_datetime
from math import radians, cos, sin, asin, sqrt


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))


@frappe.whitelist(allow_guest=True)
def create_booking():
    data = frappe.local.form_dict
    providers = frappe.get_all(
        "Service Provider",
        filters={"availability_status": "Available"},
        fields=["name", "rating", "latitude", "longitude"]
    )

    best_provider, best_score, best_distance = None, 999999, 0
    for p in providers:
        distance = calculate_distance(
            float(data.latitude), float(data.longitude),
            p.latitude, p.longitude
        )
        score = distance - (p.rating or 0)
        if score < best_score:
            best_score, best_provider, best_distance = score, p, distance

    if not best_provider:
        frappe.throw("No available providers found")

    category_docname = frappe.db.get_value(
        "Service Category",
        {"category_name": data.service_category},
        "name"
    )

    category = frappe.get_doc(
        "Service Category",
        category_docname
    )
    price = category.base_price + (best_distance * category.price_per_km)

    booking = frappe.get_doc({
        "doctype": "Service Booking",
        "customer_name": data.customer_name,
        "customer_phone": data.customer_phone,
        "service_category": data.service_category,
        "latitude": data.latitude,
        "longitude": data.longitude,
        "assigned_provider": best_provider.name,
        "distance": best_distance,
        "price": price,
        "status": "Pending",
        "booking_time": now_datetime()
    })
    booking.insert(ignore_permissions=True)

    frappe.sendmail(
        recipients=["admin@example.com"],
        subject="New Booking Created",
        message=f"Booking {booking.name} has been created for {data.customer_name}."
    )

    return {"status": "success", "booking_id": booking.name, "price": price}


@frappe.whitelist(allow_guest=True)
def get_available_providers():
    data = frappe.local.form_dict
    user_lat = float(data.get("latitude", 0))
    user_lon = float(data.get("longitude", 0))

    providers = frappe.get_all(
        "Service Provider",
        filters={"availability_status": "Available"},
        fields=["name", "provider_name", "provider_type",
                "rating", "latitude", "longitude", "phone"]
    )

    result = []
    for p in providers:
        dist = calculate_distance(user_lat, user_lon, p.latitude, p.longitude)
        result.append({
            "id": p.name,
            "name": p.provider_name,
            "type": p.provider_type,
            "rating": p.rating,
            "distance_km": round(dist, 2),
            "phone": p.phone
        })

    # Sort by distance
    result.sort(key=lambda x: x["distance_km"])
    return {"status": "success", "providers": result}


@frappe.whitelist()
def accept_booking():
    data = frappe.local.form_dict
    booking = frappe.get_doc("Service Booking", data.booking_id)

    if booking.status != "Pending":
        frappe.throw(f"Booking is already {booking.status}")

    booking.status = "Accepted"
    booking.save(ignore_permissions=True)

    frappe.sendmail(
        recipients=["admin@example.com"],
        subject=f"Booking {booking.name} Accepted",
        message=f"Your booking has been accepted by provider {booking.assigned_provider}."
    )

    return {"status": "success", "message": f"Booking {booking.name} accepted"}



@frappe.whitelist(allow_guest=True)
def booking_status():
    booking_id = frappe.local.form_dict.get("booking_id")
    booking = frappe.get_doc("Service Booking", booking_id)

    return {
        "booking_id": booking.name,
        "customer_name": booking.customer_name,
        "status": booking.status,
        "assigned_provider": booking.assigned_provider,
        "price": booking.price,
        "distance": booking.distance,
        "booking_time": str(booking.booking_time)
    }