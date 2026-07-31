import frappe
from frappe.model.document import Document

class AirplaneTicket(Document):

    def before_naming(self):
        if self.flight:
            flight = frappe.get_doc("Airplane Flight", self.flight)
            self.source_airport_code = flight.source_airport_code
            self.destination_airport_code = flight.destination_airport_code

    def validate(self):
        unique_items = []
        seen = set()

        for addon in self.add_ons:
            if addon.item not in seen:
                seen.add(addon.item)
                unique_items.append(addon)

        self.add_ons = unique_items

    def before_save(self):
        total = self.flight_price or 0

        for addon in self.add_ons:
            total += addon.amount or 0

        self.total_amount = total

    def on_submit(self):
        if self.status != "Boarded":
            frappe.throw("Only boarded tickets can be submitted.")