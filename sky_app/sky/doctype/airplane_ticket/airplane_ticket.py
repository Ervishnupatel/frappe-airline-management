import re

def validate(self):
    if not re.match(r"^[0-9]+[A-Z]$", self.seat):
        frappe.throw("Invalid seat number format")