$('#submitJobTest').click(submitJobTest);
frappe.provide("frappe.job_test");

(function onload() {
	// settings up question_name, question_type map
	frappe.job_test.question_types = {};
	frappe.job_test.questions.forEach(question => {
		frappe.job_test.question_types[question.name] = question.question_type;
	});
})();

async function submitJobTest(e) {
	frappe.confirm("Are you sure, you want to continue?", function () {
		const formData = getFormData();
		// TODO: validation
		const submission = {
			job_applicant: frappe.job_test.job_applicant,
			job_test: frappe.job_test.docname,
			answers: formData,
		};
		console.log(submission);
		frappe.call({
			method: "recruitment_ext.api.job_test.submit_job_test",
			args: { submission },
			callback: function (res) {
				console.log(res);
			},
		});
	});
}

function getFormData() {
	return $("form#jobTest").serializeArray().reduce(function (answers, input) {
		const questionType = frappe.job_test.question_types[input.name];

		if (questionType === "Multi Select") {
			if (!(input.name in answers))
				answers[input.name] = [];

			answers[input.name] = [...answers[input.name], input.value];
			return answers;
		}

		answers[input.name] = input.value;
		return answers;
	}, {});
}
