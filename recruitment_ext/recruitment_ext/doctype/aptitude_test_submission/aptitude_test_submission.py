# Copyright (c) 2021, Aakvatech Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document


class AptitudeTestSubmission(Document):
    def validate(self):
        self.calculate_result()
        self.validate_total_earned_points()

    def on_update_after_submit(self):
        self.validate_total_earned_points()

    def calculate_result(self):
        self.total_earned_points = sum(answer.earned_points for answer in self.answers)

        if self.total_points:
            self.result_percentage = flt(
                self.total_earned_points / self.total_points * 100, 2
            )

    def validate_total_earned_points(self):
        if self.total_earned_points > self.total_points:
            frappe.throw("Earned Points can no be greater than Total Points!")
