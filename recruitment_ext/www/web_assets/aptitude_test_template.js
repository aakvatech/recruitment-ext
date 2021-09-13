frappe.provide("frappe.aptitude_test_template");
$(document).ready(onload);
function onload() {
	if (frappe.aptitude_test_template.has_submitted)
		return handle_success();

	$("form#AptitudeTest").on('submit', submitAptitudeTest);

	// settings up question_name, question_type map
	frappe.aptitude_test_template.question_types = {};
	frappe.aptitude_test_template.questions.forEach(question => {
		frappe.aptitude_test_template.question_types[question.name] = question.question_type;
	});
}

function submitAptitudeTestTemplate(e) {
	e.preventDefault();
	const form = $("form#AptitudeTestTemplate")[0];
	if (!form.checkValidity()) {
		form.classList.add('was-validated');
		return;
	}


	form.classList.add('was-validated');
	frappe.confirm("Are you sure you want to continue?", function () {
		const submission = {
			job_applicant: frappe.aptitude_test_template.job_applicant,
			aptitude_test_template: frappe.aptitude_test_template.docname,
			answers: getFormData(),
		};

		frappe.call({
			method: "recruitment_ext.www.aptitude_test_template.submit_aptitude_test_template",
			args: { submission },
			callback(res) {
				if (res.exc) return;
				handle_success();
			}
		});
	});
}

function getFormData() {
	return $("form#AptitudeTestTemplate").serializeArray().reduce(function (answers, input) {
		const questionType = frappe.aptitude_test_template.question_types[input.name];

		if (questionType === "MCQ - Multiple Answers") {
			if (!(input.name in answers))
				answers[input.name] = [];

			answers[input.name] = [...answers[input.name], input.value];
			return answers;
		}

		answers[input.name] = input.value;
		return answers;
	}, {});
}

function handle_success() {
	const success_html = `
					<div class="container">
						<div class="page-card">
							<h5 class="page-card-head">
								<span class="indicator green">
									Success
								</span>
							</h5>
							<div class="page-card-body">
								<p>Thanks for taking the test! We will get in touch shortly.</p>
							</div>
						</div>
					</div>
				`;
	$(".aptitude-test-template-form-wrapper").html(success_html);
	$(".alert.alert-warning").remove();
}
