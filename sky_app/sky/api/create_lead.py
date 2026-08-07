import frappe
from frappe import _
from frappe.utils import validate_email_address, strip_html


@frappe.whitelist(allow_guest=True)
def create_lead(full_name, work_email, company=None,
                current_system=None, hoping_to_solve=None):
    """Create a CRM Lead from the public marketing form."""

    full_name = (full_name or "").strip()
    work_email = (work_email or "").strip()

    # --- validation ---
    if not full_name or not work_email:
        frappe.throw(_("Full Name and Work Email are required."))

    if not validate_email_address(work_email):
        frappe.throw(_("Please enter a valid email address."))

    # --- skip duplicates for the same email ---
    existing = frappe.db.get_value("Lead", {"email_id": work_email}, "name")
    if existing:
        return {"success": True, "duplicate": True, "lead": existing}

    # --- build the Lead ---
    parts = full_name.split(" ", 1)

    lead = frappe.new_doc("Lead")
    lead.first_name = parts[0]
    if len(parts) > 1:
        lead.last_name = parts[1]
    lead.lead_name = full_name
    lead.email_id = work_email
    lead.company_name = company
    lead.custom_current_system = current_system
    lead.custom_hoping_to_solve = strip_html(hoping_to_solve or "")
    lead.status = "Lead"

    # optional: only set if you've created a "Website" Lead Source
    if frappe.db.exists("Lead Source", "Website"):
        lead.source = "Website"

    lead.insert(ignore_permissions=True)
    frappe.db.commit()

    return {"success": True, "duplicate": False, "lead": lead.name}