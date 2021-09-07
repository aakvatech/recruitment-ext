# Copyright (c) 2021, Aakvatech Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InterviewRecord(Document):
	def on_submit(self):
		self.set_total_score_to_job_applicant()
	
	def validate(self):
		self.validate_total_interview_score()

	def validate_total_interview_score(self):
		if self.total_interview_score > self.total_benchmark_score:
			frappe.throw("Total Interview Score can not be greater than Total Benchmark Score!")

	def set_total_score_to_job_applicant(self):
		frappe.db.set_value(
            "Job Applicant", 
            self.candidate,
            'interview_score', 
            self.total_interview_score
        )
	