import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields



def after_install():
    make_custom_fields()
    frappe.db.commit()



def make_custom_fields():
    custom_fields = {
        "Job Opening": [
            {
                "fieldname": "aptitude_test_template",
                "label": "Aptitude Test Template",
                "fieldtype": "Link",
                "options": "Aptitude Test Template",
                "insert_after": "department",
            },
        ],
    }

    create_custom_fields(custom_fields)
