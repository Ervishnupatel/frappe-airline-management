import frappe, requests
from frappe.utils import get_url

def sync_employee_to_cms(doc, method=None):
    # enqueue so saving an Employee isn't blocked by the HTTP call
    frappe.enqueue(_post_employee, doc_name=doc.name, queue="short", enqueue_after_commit=True,)

def _post_employee(doc_name):
    doc = frappe.get_doc("Employee", doc_name)
    url    = frappe.conf.get("cms_employee_webhook_url")  # e.g. https://yoursite.com/webhooks/frappe/employee
    secret = frappe.conf.get("cms_webhook_secret")        # must equal FRAPPE_WEBHOOK_SECRET
    if not (url and secret):
        return
    payload = {
        "employee_id":   doc.name,
        "employee_name": doc.employee_name,
        "designation":   doc.designation,
        "image":         get_url(doc.image),
    }
    try:
        requests.post(url, json=payload, headers={"x-frappe-webhook-secret": secret}, timeout=10)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "CMS employee sync failed")

def delete_employee_from_cms(doc, method=None):
    # Capture the docname now and only fire after commit — if the delete rolls
    # back, we must NOT have already removed it from the CMS.
    frappe.enqueue(
        _delete_employee,
        doc_name=doc.name,
        queue="short",
        enqueue_after_commit=True,
    )


def _delete_employee(doc_name):
    url    = frappe.conf.get("cms_employee_webhook_url")
    secret = frappe.conf.get("cms_webhook_secret")
    if not (url and secret):
        return
    # The doc is already gone here, so we only send its name — no get_doc.
    resp = requests.delete(
        url,
        json={"employee_id": doc_name},
        headers={"x-frappe-webhook-secret": secret},
        timeout=10,
    )
    if resp.status_code >= 400:
        frappe.throw(f"CMS employee delete failed [{resp.status_code}]: {resp.text}")