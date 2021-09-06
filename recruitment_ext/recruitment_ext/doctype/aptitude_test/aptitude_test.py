# Copyright (c) 2021, Aakvatech Limited and contributors
# For license information, please see license.txt
import json

import frappe
from frappe.model.document import Document


class AptitudeTest(Document):
    def before_save(self):
        self.total_points = sum(question.points for question in self.questions)
