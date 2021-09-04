frappe.provide("frappe.aptitude_test");
$(document).ready(onload);
function onload() {
	$("form#AptitudeTest").on('submit', submitAptitudeTest)

	// settings up question_name, question_type map
	frappe.aptitude_test.question_types = {};
	frappe.aptitude_test.questions.forEach(question => {
		frappe.aptitude_test.question_types[question.name] = question.question_type;
	});
}

function submitAptitudeTest(e) {
	e.preventDefault();
	frappe.confirm("Are you sure you want to continue?", function () {
		const submission = {
			job_applicant: frappe.aptitude_test.job_applicant,
			aptitude_test: frappe.aptitude_test.docname,
			answers: getFormData(),
		};

		frappe.call({
			method: "recruitment_ext.www.aptitude_test.submit_aptitude_test",
			args: { submission },
		});
	});
}

function getFormData() {
	return $("form#AptitudeTest").serializeArray().reduce(function (answers, input) {
		const questionType = frappe.aptitude_test.question_types[input.name];

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
