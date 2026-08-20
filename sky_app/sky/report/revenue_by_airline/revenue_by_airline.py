# Copyright (c) 2026, xzy and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType
from frappe.query_builder.functions import Coalesce, Sum


def execute(filters=None):
	columns = get_columns()
	data = get_data()
	total_revenue = sum(row["revenue"] for row in data)

	report_summary = [{"label": _("Total Revenue"), "value": total_revenue, "indicator": "Green", "datatype": "Currency"}]
	chart = {
		"data": {
			"labels": [row["airline"] for row in data],
			"datasets": [{"name": _("Revenue"), "values": [row["revenue"] for row in data]}],
		},
		"type": "donut",
	}
	return columns, data, None, chart, report_summary


def get_columns():
	return [
		{"label": _("Airline"), "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
		{"label": _("Revenue"), "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
	]


def get_data():
	airline = DocType("Airline")
	airplane = DocType("Airplane")
	flight = DocType("Airplane Flight")
	ticket = DocType("Airplane Ticket")
	return (
		frappe.qb.from_(airline)
		.left_join(airplane)
		.on(airplane.airline == airline.name)
		.left_join(flight)
		.on(flight.airplane == airplane.name)
		.left_join(ticket)
		.on((ticket.flight == flight.name) & (ticket.docstatus == 1))
		.select(airline.name.as_("airline"), Coalesce(Sum(ticket.total_amount), 0).as_("revenue"))
		.groupby(airline.name)
		.run(as_dict=True)
	)
