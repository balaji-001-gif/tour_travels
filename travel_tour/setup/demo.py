import frappe

def create_demo_data():
    """
    Populates standard demo data for the Travel Tour application
    so users don't have to manually create the base entities.
    """
    frappe.flags.in_test = True

    try:
        # 1. Create Destinations
        print("Creating Destinations...")
        destinations = [
            {"doctype": "Destination", "destination_name": "Dubai", "country": "United Arab Emirates", "status": "Active"},
            {"doctype": "Destination", "destination_name": "Maldives", "country": "Maldives", "status": "Active"},
            {"doctype": "Destination", "destination_name": "Switzerland", "country": "Switzerland", "status": "Active"}
        ]
        
        for d in destinations:
            if not frappe.db.exists("Destination", d["destination_name"]):
                frappe.get_doc(d).insert(ignore_permissions=True)

        # 2. Create Tour Packages
        print("Creating Tour Packages...")
        packages = [
            {
                "doctype": "Tour Package",
                "package_name": "Majestic Dubai Escape",
                "destination": "Dubai",
                "duration_days": 5,
                "duration_nights": 4,
                "status": "Active",
                "inclusion": "Hotel, Meals, Desert Safari, Burj Khalifa",
                "exclusion": "Flights, Visa",
                "itinerary": [
                    {"day_number": 1, "title": "Arrival", "description": "Airport transfer to hotel."},
                    {"day_number": 2, "title": "City Tour", "description": "Burj Khalifa and Dubai Mall."},
                    {"day_number": 3, "title": "Desert Safari", "description": "Dune bashing and BBQ dinner."}
                ],
                "pricing": [
                    {"pax_range": "1", "price_per_pax": 1200},
                    {"pax_range": "2-4", "price_per_pax": 1000}
                ]
            },
            {
                "doctype": "Tour Package",
                "package_name": "Romantic Maldives Retreat",
                "destination": "Maldives",
                "duration_days": 4,
                "duration_nights": 3,
                "status": "Active",
                "inclusion": "Water Villa, Seaplane transfer, All-inclusive meals",
                "itinerary": [
                    {"day_number": 1, "title": "Arrival", "description": "Seaplane to resort."},
                    {"day_number": 2, "title": "Leisure", "description": "Snorkeling and spa."}
                ]
            }
        ]

        for p in packages:
            if not frappe.db.exists("Tour Package", p["package_name"]):
                frappe.get_doc(p).insert(ignore_permissions=True)

        # 3. Create Travel Leads
        print("Creating Demo Lead...")
        if not frappe.db.exists("Travel Lead", {"email_id": "demo@example.com"}):
            frappe.get_doc({
                "doctype": "Travel Lead",
                "customer_name": "Demo Client",
                "email_id": "demo@example.com",
                "mobile_no": "+1234567890",
                "suggested_package": "Majestic Dubai Escape",
                "pax_count": 2,
                "status": "Open",
                "source": "Website"
            }).insert(ignore_permissions=True)


        # 4. Create Visa Country Config
        print("Creating Visa Configs...")
        visa_configs = [
            {
                "doctype": "Visa Country Config",
                "country": "United Arab Emirates",
                "visa_type": "Tourist",
                "processing_time_days": 3,
                "base_fee": 100,
                "required_documents": [
                    {"document_name": "Passport Copy - Front & Back", "is_mandatory": 1},
                    {"document_name": "Passport Size Photograph", "is_mandatory": 1}
                ]
            }
        ]
        for vc in visa_configs:
            if not frappe.db.exists("Visa Country Config", vc["country"]):
                frappe.get_doc(vc).insert(ignore_permissions=True)


        frappe.db.commit()
        print("\n✅ Success! Demo Data has been fully populated in the site.")
        
    except Exception as e:
        print(f"\n❌ Error populating demo data: {e}")
        frappe.db.rollback()

