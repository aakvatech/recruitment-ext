# Copyright (c) 2021, Aakvatech Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt, cint
from frappe.model.document import Document

class InterviewRecord(Document):
	def on_submit(self):
		self.set_average_score()
	
	def validate(self):
		self.validate_total_interview_score()
		self.create_scores()

	def validate_total_interview_score(self):
		if self.total_interview_score > self.total_benchmark_score:
			frappe.throw("Total Interview Score can not be greater than Total Benchmark Score!")

	
	def create_scores(doc):
		if not frappe.db.exists("Interview Mark", {"record_no": doc.name}):
			applicant = frappe.get_doc("Job Applicant", doc.job_applicant)
			applicant.append("scores", {
				"record_no": doc.name,
				"interviewer": doc.interviewer,
				"marks": doc.total_interview_score,
				"parent": doc.job_applicant,
				"parenttype": "Job Applicant"
			})
			applicant.save(ignore_permissions=True)
			
	
	def set_average_score(self):
		score = 0
		total_marks = frappe.get_list("Interview Mark", {"parent": self.job_applicant}, "marks")
		frappe.msgprint("total_marks: " + str(average_score))

		number_of_rows = len(total_marks)
		frappe.msgprint("number_of_rows: " + str(number_of_rows))

		for mark in total_marks:
			score += cint(mark.marks)
			average_score = flt(score/number_of_rows)
			frappe.msgprint("average score: " + str(average_score))

			frappe.db.set_value(
				"Job Applicant",
				self.job_applicant, 
				"overall_score",
				average_score
			)

		