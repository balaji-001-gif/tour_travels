import frappe
from frappe import _

def on_submit(doc, method):
    """
    Called when a Booking is submitted.
    Creates internal records like Sales Invoice (if not already managed by ERPNext core)
    """
    doc.update_lead_status()

def on_cancel(doc, method):
    """
    Called when a Booking is cancelled.
    Should handle refund logic or cancellation fees.
    """
    pass

def create_visa_applications(doc, method):
    """
    Auto-creates Visa Application records for international tours.
    """
    pkg = frappe.get_doc('Tour Package', doc.tour_package)
    if not pkg.visa_required:
        return

    for pax in doc.pax_details:
        # Create a Visa Application for each pax
        v_app = frappe.get_doc({
            'doctype': 'Visa Application',
            'booking': doc.name,
            'applicant_name': pax.pax_name,
            'passport_number': pax.passport_number,
            'passport_expiry': pax.passport_expiry,
            'destination_country': pkg.destination, # Assuming destination links to a country or is a country
            'departure_date': doc.departure_date,
            'status': 'Pending Documents'
        })
        v_app.insert(ignore_permissions=True)
    
    frappe.msgprint(_("Created Visa Applications for {0} passengers").format(len(doc.pax_details)))

def allocate_allotments(doc, method):
    """
    Allocates hotel allotments for the booking.
    """
    pass

def send_confirmation_whatsapp(doc, method):
    """
    Sends booking confirmation via WhatsApp logic.
    """
    # Placeholder for WhatsApp API logic
    pass

def create_run_sheet(doc, method):
    """
    Creates a Trip Run Sheet for the operations team.
    """
    run_sheet = frappe.get_doc({
        'doctype': 'Trip Run Sheet',
        'booking': doc.name,
        'customer': doc.customer,
        'departure_date': doc.departure_date,
        'total_pax': doc.total_pax
    })
    run_sheet.insert(ignore_permissions=True)

# Helper method on DocType class might be better, but we can extend it here
def update_lead_status(doc):
    # If the booking was converted from a lead, mark the lead as converted
    pass
