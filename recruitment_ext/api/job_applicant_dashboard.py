from frappe import _


def get_data(data):
    return {
        "fieldname": "job_applicant",
        "transactions": [
            {
                "label": _("Aptitude Test"),
                "items": [
                    "Aptitude Test Submission",
                ],
            },
        ],
    }
