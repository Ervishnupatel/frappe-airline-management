import frappe
from frappe.model.document import Document
frappe.msgprint("before_save is running")

class AirplaneTicket(Document):

    def before_save(self):
        frappe.msgprint("before_save is running")

        total = self.flight_price or 0

        for addon in self.add_ons:
            total += addon.amount or 0

        self.total_amount = total