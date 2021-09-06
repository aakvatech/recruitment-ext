frappe.ready(() => {
	// TODO: check if Job Opening has Aptitude Test
	if (frappe.web_form.doc_type !== "Job Applicant") {
		frappe.web_form.handle_success = (doc) => {
			window.location.assign(`/aptitude_test?job_applicant=${doc.name}&job_opening=${doc.job_title}`);
		};
	}
});

