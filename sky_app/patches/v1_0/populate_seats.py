import frappe
import random


def execute():

    tickets = frappe.get_all(
        "Airplane Ticket",
        fields=["name", "seat"]
    )

    for ticket in tickets:

        if not ticket.seat:

            random_number = random.randint(1, 99)

            random_letter = random.choice(
                ["A", "B", "C", "D", "E"]
            )

            seat = f"{random_number}{random_letter}"

            frappe.db.set_value(
                "Airplane Ticket",
                ticket.name,
                "seat",
                seat
            )

    frappe.db.commit()
