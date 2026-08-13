import frappe


def execute(filters=None):
    columns = [
        {
            "label": "Airline",
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200,
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 150,
        },
    ]

    airlines = frappe.get_all(
        "Airline",
        fields=["name"],
    )

    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"docstatus": 1},
        fields=["flight", "total_amount"],
    )

    flights = frappe.get_all(
        "Airplane Flight",
        fields=["name", "airplane"],
    )

    airplanes = frappe.get_all(
        "Airplane",
        fields=["name", "airline"],
    )

    flight_to_airplane = {
        flight.name: flight.airplane
        for flight in flights
    }

    airplane_to_airline = {
        airplane.name: airplane.airline
        for airplane in airplanes
    }

    revenue = {
        airline.name: 0
        for airline in airlines
    }

    for ticket in tickets:
        airplane = flight_to_airplane.get(ticket.flight)

        if not airplane:
            continue

        airline = airplane_to_airline.get(airplane)

        if not airline:
            continue

        revenue[airline] += ticket.total_amount or 0

    data = [
        {
            "airline": airline.name,
            "revenue": revenue[airline.name],
        }
        for airline in airlines
    ]

    total_revenue = sum(row["revenue"] for row in data)

    report_summary = [
        {
            "label": "Total Revenue",
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
                    "name": "Revenue",
                    "values": [row["revenue"] for row in data],
                }
            ],
        },
        "type": "donut",
    }

    return columns, data, None, chart, report_summary