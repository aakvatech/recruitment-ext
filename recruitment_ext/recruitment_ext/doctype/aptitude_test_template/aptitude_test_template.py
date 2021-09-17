# Copyright (c) 2021, Aakvatech Limited and contributors
# For license information, please see license.txt
import json

import frappe
from frappe.model.document import Document


class AptitudeTestTemplate(Document):
    def validate(self):
        for question in self.questions:
            if question.min_allowed_answers > question.max_allowed_answers:
                frappe.throw(
                    "{0} can no be greater than {1} for row #{2} in {3}".format(
                        frappe.bold("Min Allowed Answers"),
                        frappe.bold("Max Allowed Answers"),
                        frappe.bold(question.idx),
                        frappe.bold("Questions"),
                    ),
                )
        self.total_points = sum(question.points for question in self.questions)
