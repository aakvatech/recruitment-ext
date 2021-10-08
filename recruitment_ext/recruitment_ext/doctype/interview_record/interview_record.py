# Copyright (c) 2021, Aakvatech Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InterviewRecord(Document):
	def on_submit(self):
		# self.set_total_interview_score_to_job_applicant()
		self.create_scores()
	
	def validate(self):
		self.validate_total_interview_score()

	def validate_total_interview_score(self):
		if self.total_interview_score > self.total_benchmark_score:
			frappe.throw("Total Interview Score can not be greater than Total Benchmark Score!")

	# def set_total_interview_score_to_job_applicant(self):
	# 	frappe.db.set_value(
    #         "Job Applicant", 
    #         self.job_applicant,
    #         'interview_record', 
    #         self.total_interview_score
    #     )
	
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
			
		# applicant = frappe.get_doc({
			# 	"doctype": "Job Applicant",
			# 	"applicant_name": doc.candidate_name,
			# 	"email_id": doc.candidate_email,
			# 	"status": "Open",
			# 	"scores": [
			# 		{
			# 			"record_no": doc.name,
			# 			"interviewer": doc.interviewer,
			# 			"interview_score": doc.total_interview_score,
			# 			"parent": doc.job_applicant,
			# 			"parenttype": "Job Applicant"
			# 		}
			# 	]
			# })

		# if not mark:
		# 	applicant = frappe.get_value("Job Applicant", doc.job_applicant)
			# frappe.msgprint(str(applicant))
			# score = frappe.get_doc({
			# 	"doctype": "Interview Mark",
			# 	"record_no": doc.name,
			# 	"interviewer": doc.interviewer,
			# 	"interview_score": doc.total_interview_score,
			# 	"parent": applicant,
			# 	"parenttype": "Job Applicant"
			# }).insert(ignore_permissions=True)
			# frappe.db.commit()
			# score = frappe.new_doc("Interview Mark")
			# score.record_no = doc.name,
			# score.interviewer = doc.interviewer
			# score.interview_score = doc.total_interview_score
			# score.parent = applicant
			# score.parenttype = "Job Applicant"
			# score.insert(ignore_permissions=True)
	
	# def validate_job_applicant(self):
	# 	if not frappe.db.exits("Job Applicant", self.job_applicant):
	# 		frappe.throw("Job Applicant not found for candidate {0}".format(
	# 			frappe.bold(self.job_applicant)
	# 		))

	