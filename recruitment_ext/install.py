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
        "Job Applicant": [
            {
                "fieldname": "aptitude_test_score",
                "label": "Aptitude Test Score",
                "fieldtype": "Int",
                "insert_after": "applicant_rating",
                "read_only": "1",
            },
        ],
    }

    create_custom_fields(custom_fields)
