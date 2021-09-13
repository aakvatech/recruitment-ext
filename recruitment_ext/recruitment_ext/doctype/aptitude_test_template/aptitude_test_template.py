# Copyright (c) 2021, Aakvatech Limited and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class AptitudeTestTemplate(Document):
	def before_save(self):
        self.total_points = sum(question.points for question in self.questions)
