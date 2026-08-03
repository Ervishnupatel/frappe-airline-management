import frappe
from frappe.model.document import Document


class AirplaneFlight(Document):

    def on_submit(self):
        self.db_set("status", "Completed")