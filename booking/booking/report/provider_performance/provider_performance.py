# Copyright (c) 2026, test and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": "Provider",
            "fieldname": "assigned_provider",
            "fieldtype": "Link",
            "options": "Service Provider",
            "width": 200
        },
        {
            "label": "Total Bookings",
            "fieldname": "total",
            "fieldtype": "Int",
            "width": 130
        },
        {
            "label": "Pending",
            "fieldname": "pending",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": "Accepted",
            "fieldname": "accepted",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": "Completed",
            "fieldname": "completed",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": "Cancelled",
            "fieldname": "cancelled",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": "Total Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Avg Distance (km)",
            "fieldname": "avg_distance",
            "fieldtype": "Float",
            "width": 150
        }
    ]


def get_data(filters):
    conditions = "WHERE assigned_provider IS NOT NULL"

    if filters.get("from_date"):
        conditions += " AND DATE(booking_time) >= %(from_date)s"

    if filters.get("to_date"):
        conditions += " AND DATE(booking_time) <= %(to_date)s"

    if filters.get("assigned_provider"):
        conditions += " AND assigned_provider = %(assigned_provider)s"

    if filters.get("status"):
        conditions += " AND status = %(status)s"

    data = frappe.db.sql("""
        SELECT
            assigned_provider,
            COUNT(*) as total,
            SUM(CASE WHEN status = 'Pending'   THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN status = 'Accepted'  THEN 1 ELSE 0 END) as accepted,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
            SUM(price)      as revenue,
            AVG(distance)   as avg_distance
        FROM `tabService Booking`
        {conditions}
        GROUP BY assigned_provider
        ORDER BY total DESC
    """.format(conditions=conditions), filters, as_dict=True)

    return data