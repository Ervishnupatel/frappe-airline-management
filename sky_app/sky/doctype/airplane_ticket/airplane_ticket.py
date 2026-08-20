import re
import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
    def validate(self):
        self.total_amount = frappe.utils.flt(self.flight_price) + sum(
            frappe.utils.flt(add_on.amount) for add_on in self.get("add_ons")
        )

        # Validate seat format
        if self.seat and not re.match(r"^[0-9]+[A-Z]$", self.seat):
            frappe.throw("Invalid seat number format")

    def before_insert(self):
        airplane = frappe.db.get_value(
            "Airplane Flight",
            self.flight,
            "airplane"
        )

        capacity = frappe.db.get_value(
            "Airplane",
            airplane,
            "capacity"
        )

        ticket_count = frappe.db.count(
            "Airplane Ticket",
            {
                "flight": self.flight,
                "docstatus": ["!=", 2]
            }
        )

        if ticket_count >= capacity:
            frappe.throw("This flight is fully booked.")

