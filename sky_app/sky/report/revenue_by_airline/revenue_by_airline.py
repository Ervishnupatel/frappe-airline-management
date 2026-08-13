# Copyright (c) 2026, xzy and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data()

	total_revenue = sum(row["revenue"] for row in data)

	report_summary = [
		{
			"label": _("Total Revenue"),
			"value": total_revenue,
			"indicator": "Green",
			"datatype": "Currency",
		}
	]

	chart = {
		"data": {
			"labels": [row["airline"] for row in data],
			"datasets": [
				{
					"name": _("Revenue"),
					"values": [row["revenue"] for row in data],
				}
			],
		},
		"type": "donut",
	}

	return columns, data, None, chart, report_summary


def get_columns():
	return [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
			"width": 200,
		},
		{
			"label": _("Revenue"),
			"fieldname": "revenue",
			"fieldtype": "Currency",
			"width": 150,
		},
	]


def get_data():
	# Get all airlines so airlines with zero revenue are included
	airlines = frappe.get_all(
		"Airline",
		fields=["name"],
	)

	# Get only submitted Airplane Tickets
	tickets = frappe.get_all(
		"Airplane Ticket",
		filters={"docstatus": 1},
		fields=["flight", "total_amount"],
	)

	# Get all Airplane Flights
	flights = frappe.get_all(
		"Airplane Flight",
		fields=["name", "airplane"],
	)

	# Get all Airplanes and their Airlines
	airplanes = frappe.get_all(
		"Airplane",
		fields=["name", "airline"],
	)

	# Flight → Airplane
	flight_to_airplane = {
		flight.name: flight.airplane
		for flight in flights
	}

	# Airplane → Airline
	airplane_to_airline = {
		airplane.name: airplane.airline
		for airplane in airplanes
	}

	# Start every airline with zero revenue
	revenue = {
		airline.name: 0
		for airline in airlines
	}

	# Add submitted ticket revenue to the correct airline
	for ticket in tickets:
		airplane = flight_to_airplane.get(ticket.flight)

		if not airplane:
			continue

		airline = airplane_to_airline.get(airplane)

		if not airline:
			continue

		revenue[airline] += ticket.total_amount or 0

	# Create report rows
	return [
		{
			"airline": airline.name,
			"revenue": revenue[airline.name],
		}
		for airline in airlines
	]