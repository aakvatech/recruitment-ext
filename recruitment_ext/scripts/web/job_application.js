
frappe.ready(() => {
	const { job_title } = frappe.utils.get_query_params();
	if (!job_title) return;

	// If Job Opening has Aptitude Test Template, redirect to the respective Aptitude Test Template
	frappe.call({
		method: 'recruitment_ext.www.aptitude_test.get_aptitude_test',
		args: { job_opening: job_title },
		callback({ message }) {
			if (!message) return;
			frappe.web_form.handle_success = (doc) => {
				window.location.assign(`/aptitude_test_template?job_applicant=${doc.name}&job_opening=${doc.job_title}`);
			};
		}
	});
});

