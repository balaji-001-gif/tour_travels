import frappe
from frappe.utils import today, add_days, getdate
import random

def create_demo_data():
    """
    Populates extensive demo data (5-10 records per DocType) for the Travel Tour application.
    """
    frappe.flags.in_test = True

    try:
        # ────────── 1. DESTINATIONS (10) ──────────
        print("Creating 10 Destinations...")
        destinations = [
            ("Dubai", "United Arab Emirates"), ("Maldives", "Maldives"), ("Switzerland", "Switzerland"),
            ("Thailand", "Thailand"), ("Singapore", "Singapore"), ("Malaysia", "Malaysia"),
            ("Bali", "Indonesia"), ("Paris", "France"), ("London", "United Kingdom"), ("New York", "United States")
        ]
        
        for dest, country in destinations:
            if not frappe.db.exists("Destination", dest):
                frappe.get_doc({
                    "doctype": "Destination", "destination_name": dest, "country": country, "status": "Active"
                }).insert(ignore_permissions=True)

        # ────────── 2. TOUR PACKAGES (10) ──────────
        print("Creating 10 Tour Packages...")
        packages = []
        for i, (dest, country) in enumerate(destinations):
            pkg_name = f"Signature {dest} Premium Tour"
            if not frappe.db.exists("Tour Package", pkg_name):
                doc = frappe.get_doc({
                    "doctype": "Tour Package",
                    "package_name": pkg_name,
                    "destination": dest,
                    "duration_days": random.randint(4, 7),
                    "duration_nights": random.randint(3, 6),
                    "status": "Active",
                    "tour_type": "International",
                    "description": "Premium Hotel, Daily Breakfast, Guided Tours, Transfers",
                    "itinerary": [
                        {"day_number": 1, "title": "Arrival", "description": f"Welcome to {dest}. Airport transfer to luxury hotel."},
                        {"day_number": 2, "title": "City Highlights", "description": f"Exploring the premium zones of {dest}."},
                        {"day_number": 3, "title": "Leisure & Shopping", "description": "Free time for leisure activities."}
                    ],
                    "pricing_table": [
                        {"min_pax": 1, "max_pax": 2, "per_person_price": random.randint(1000, 2000)},
                        {"min_pax": 3, "max_pax": 10, "per_person_price": random.randint(800, 1500)}
                    ]
                }).insert(ignore_permissions=True)
                packages.append(doc)

        # ────────── 3. TRAVEL LEADS (10) ──────────
        print("Creating 10 Travel Leads...")
        lead_names = ["Alice Smith", "Bob Johnson", "Charlie Davis", "Diana Prince", "Eve Adams", 
                      "Frank Castle", "Grace Hopper", "Hank Pym", "Ivy Fern", "Jack Sparrow"]
        
        leads = []
        for i, name in enumerate(lead_names):
            if not frappe.db.exists("Travel Lead", {"email_id": f"client{i}@example.com"}):
                doc = frappe.get_doc({
                    "doctype": "Travel Lead",
                    "customer_name": name,
                    "email_id": f"client{i}@example.com",
                    "mobile_no": f"+100000000{i}",
                    "suggested_package": f"Signature {destinations[i][0]} Premium Tour",
                    "pax_count": random.randint(1, 4),
                    "status": random.choice(["Open", "Interested", "converted", "Lost"]),
                    "source": random.choice(["Website", "Referral", "Social Media"])
                }).insert(ignore_permissions=True)
                leads.append(doc)

        # ────────── 4. SUPPLIER CONTRACTS (5) ──────────
        print("Creating 5 Supplier Contracts...")
        suppliers = ["Marriott International", "Hilton Hotels", "Emirates Transport", "Skyline Tours", "Oceanic Voyages"]
        
        for i, supp in enumerate(suppliers):
            # Ensure the core Supplier exists first
            if not frappe.db.exists("Supplier", supp):
                frappe.get_doc({
                    "doctype": "Supplier",
                    "supplier_name": supp,
                    "supplier_group": "All Supplier Groups"
                }).insert(ignore_permissions=True)

            if not frappe.db.exists("Supplier Contract", {"supplier": supp}):
                frappe.get_doc({
                    "doctype": "Supplier Contract",
                    "supplier": supp,
                    "supplier_name": supp,
                    "cost_per_pax": random.randint(100, 500),
                    "contract_start_date": today(),
                    "contract_end_date": add_days(today(), 365)
                }).insert(ignore_permissions=True)

        # ────────── 5. VISA CONFIGS (5) ──────────
        print("Creating 5 Visa Country Configs...")
        for dest, country in destinations[:5]:
            if not frappe.db.exists("Visa Country Config", {"country": country, "visa_type": "Tourist"}):
                frappe.get_doc({
                    "doctype": "Visa Country Config",
                    "country": country,
                    "visa_type": "Tourist",
                    "processing_time_days": 5,
                    "base_fee": random.randint(50, 150),
                    "required_documents": [
                        {"document_name": "Passport Copy - Front & Back", "is_mandatory": 1},
                        {"document_name": "Photograph (White Background)", "is_mandatory": 1},
                        {"document_name": "6 Months Bank Statement", "is_mandatory": 0}
                    ]
                }).insert(ignore_permissions=True)

        # ────────── 6. BOOKINGS (5) ──────────
        print("Creating 5 Confirmed Bookings...")
        for i in range(5):
            lead = leads[i]
            
            # Ensure Customer exists
            if not frappe.db.exists("Customer", lead.customer_name):
                frappe.get_doc({
                    "doctype": "Customer",
                    "customer_name": lead.customer_name,
                    "customer_group": "All Customer Groups",
                    "customer_type": "Individual",
                    "territory": "All Territories"
                }).insert(ignore_permissions=True)

            if not frappe.db.exists("Booking", {"travel_lead": lead.name}):
                bk = frappe.get_doc({
                    "doctype": "Booking",
                    "customer": lead.customer_name,
                    "travel_lead": lead.name,
                    "tour_package": lead.suggested_package,
                    "departure_date": add_days(today(), random.randint(10, 30)),
                    "total_pax": lead.pax_count,
                    "booking_status": "Confirmed",
                    "pax_details": [
                        {"pax_name": lead.customer_name, "pax_age": 30, "passport_number": f"P{1000+i}X"},
                        {"pax_name": f"{lead.customer_name} Partner", "pax_age": 28, "passport_number": f"P{2000+i}Y"}
                    ] if lead.pax_count > 1 else [
                        {"pax_name": lead.customer_name, "pax_age": 30, "passport_number": f"P{1000+i}X"}
                    ]
                }).insert(ignore_permissions=True)
                
                # Create related operational docs
                print(f"Creating Operational Docs for Booking: {bk.name}")
                
                # 7. VISA APPLICATION
                frappe.get_doc({
                    "doctype": "Visa Application",
                    "booking": bk.name,
                    "passenger_name": lead.customer_name,
                    "country": destinations[i][1],
                    "status": "Document Collection",
                    "visa_type": "Tourist",
                    "application_date": today(),
                    "expected_arrival_date": add_days(today(), 5)
                }).insert(ignore_permissions=True)
                
                # 8. HOTEL ALLOTMENT
                frappe.get_doc({
                    "doctype": "Hotel Allotment",
                    "booking": bk.name,
                    "hotel_name": suppliers[i % 2],
                    "check_in_date": bk.departure_date,
                    "check_out_date": add_days(bk.departure_date, 3),
                    "status": "Requested",
                    "rooms": [
                        {"room_type": "Deluxe Double", "quantity": 1, "occupancy": "Double" if lead.pax_count > 1 else "Single"}
                    ]
                }).insert(ignore_permissions=True)
                
                # 9. TRIP RUN SHEET
                frappe.get_doc({
                    "doctype": "Trip Run Sheet",
                    "booking": bk.name,
                    "tour_start_date": bk.departure_date,
                    "tour_end_date": add_days(bk.departure_date, 5),
                    "status": "Draft",
                    "daily_schedule": [
                        {"day_number": 1, "date": bk.departure_date, "activity": "Airport Transfer"}
                    ]
                }).insert(ignore_permissions=True)

        frappe.db.commit()
        print("\n✅ Success! 5 to 10 records for EVERY major DocType have been generated!")
        
    except Exception as e:
        print(f"\n❌ Error populating demo data: {e}")
        frappe.db.rollback()

