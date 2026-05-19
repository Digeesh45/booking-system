// Copyright (c) 2026, test and contributors
// For license information, please see license.txt

frappe.query_reports["Provider Performance"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_start(),
            "reqd": 0
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.now_date(),
            "reqd": 0
        },
        {
            "fieldname": "assigned_provider",
            "label": __("Provider"),
            "fieldtype": "Link",
            "options": "Service Provider",
            "reqd": 0
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nPending\nAccepted\nCompleted\nCancelled",
            "reqd": 0
        }
    ]
};