# Copyright (c) 2021, Aakvatech Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt, cint
from frappe.model.document import Document

class InterviewRecord(Document):
	def on_submit(self):
		self.create_scores()
	
	def validate(self):
		self.validate_total_interview_score()

	def validate_total_interview_score(self):
		if self.total_interview_score > self.total_benchmark_score:
			frappe.throw("Total Interview Score can not be greater than Total Benchmark Score!")

	
	def create_scores(doc):
		if not frappe.db.exists("Interview Mark", {"record_no": doc.name}):
			applicant = frappe.get_doc("Job Applicant", doc.job_applicant)
			applicant.append("scores", {
				"record_no": doc.name,
				"interview_date": doc.date_time_of_interview,
				"interviewer": doc.interviewer,
				"benchmark_score": doc.total_benchmark_score,
				"interview_score": doc.total_interview_score,
				"parent": doc.job_applicant,
				"parenttype": "Job Applicant"
			})
			applicant.save(ignore_permissions=True)
		
		score = 0
		total_marks = frappe.get_list("Interview Mark", {"parent": doc.job_applicant}, "interview_score")
		if not total_marks:
			return

		number_of_rows = len(total_marks)

		for mark in total_marks:
			score += cint(mark.interview_score)
			average_interview_score = flt(score / number_of_rows)

			frappe.db.set_value(
				"Job Applicant",
				doc.job_applicant, 
				"average_interview_score",
				average_interview_score
			)
		

		