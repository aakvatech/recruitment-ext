import json

import frappe
from frappe import bold


CONTACT_MSG = (
    "<br><br>If this seems like a mistake, please email us for support."
)


def get_context(context):
    validate_query_params()
    job_opening = frappe.get_doc("Job Opening", frappe.form_dict["job_opening"])
    aptitude_test = frappe.get_doc("Aptitude Test", job_opening.aptitude_test)

    keys_to_include = {
        "name",
        "question",
        "required",
        "question_type",
        "options",
        "placeholder_text",
    }

    # TODO: strip options
    context.update(
        {
            "docname": aptitude_test.name,
            "title": aptitude_test.title,
            "description": aptitude_test.description,
            "total_points": aptitude_test.total_points,
            "questions": [
                {key: question.get(key) for key in keys_to_include}
                for question in aptitude_test.questions
            ],
        }
    )
    # for JavaScript
    context.questions_json = json.dumps(context.questions)


@frappe.whitelist(allow_guest=True)
def submit_aptitude_test(submission):
    submission = frappe._dict(json.loads(submission))
    questions = frappe.get_all(
        "Aptitude Test Question",
        filters={"parent": submission["aptitude_test"]},
        fields=["*"],
    )
    validate_aptitude_test_submision(questions, submission)
    answers = prepare_answers(questions, submission)
    doc = frappe.get_doc(
        {
            "doctype": "Aptitude Test Submission",
            "aptitude_test": submission["aptitude_test"],
            "job_applicant": submission["job_applicant"],
            "answers": answers,
            "total_earned_points": sum(ans["earned_points"] for ans in answers),
        }
    )
    doc.flags.ignore_permissions = True
    doc.submit()

def validate_query_params():
    for key in ("job_opening", "job_applicant"):
        if key not in frappe.form_dict:
            redirect(incomplete_url=True)


def redirect(
    message="Something went wrong, please try again later.",
    title="Server Error",
    show_contact_msg=False,
    incomplete_url=False,
):
    if incomplete_url:
        title = "Some information is missing"
        message = "The URL you entered is incomplete."
        show_contact_msg = True

    if show_contact_msg:
        message += CONTACT_MSG

    frappe.redirect_to_message(title, message)
    frappe.local.flags.redirect_location = frappe.local.response.location
    raise frappe.Redirect


def prepare_answers(questions, submission):
    answers = []
    for question in questions:
        answer = {
            "question_link": question.name,
            "earned_points": 0,
        }

        if question.question_type == "MCQ - Multiple Answers":
            answer["answer"] = "\n".join(
                (
                    option.strip()
                    for option in submission["answers"].get(question.name, [])
                )
            )
        else:
            answer["answer"] = submission["answers"].get(question.name, "")

        # calculate points
        if (
            question.correct_answer
            and question.question_type != "Long Answer"
            and question.correct_answer.strip() == answer["answer"].strip()
        ):
            answer["earned_points"] = question.points

        answers.append(answer)
    return answers


def validate_aptitude_test_submision(questions, submission):
    # TODO: uncomment below validation after getting applicant from form
    # validate_job_applicant(submission)
    error_message = ""
    print(questions)
    for question in questions:
        # TODO: remove these 2 lines after adding fields to the doctype
        question.min_allowed_answers = 1
        question.max_allowed_answers = 3

        if question.required and not submission.answers.get(question.name):
            error_message += wrap_with_html_tag(
                f"The question: { bold(question.question) } is required!", "li"
            )

        if question.question_type != "MCQ - Multiple Answers":
            continue

        number_of_answers = len(submission.answers.get(question.name, []))
        if not question.required and not number_of_answers:
            continue

        if number_of_answers < question.min_allowed_answers:
            error_message += wrap_with_html_tag(
                f"choose atleast { bold(question.min_allowed_answers) } option(s) for the question: { bold(question.question) }",
                "li",
            )
        if number_of_answers > question.max_allowed_answers:
            error_message += wrap_with_html_tag(
                f"maximum { bold(question.max_allowed_answers) } option(s) allowed to choose for the question: { bold(question.question) }",
                "li",
            )

    if error_message:
        error_message = (
            f"Following Questions have errors: <br><br><ul> {error_message} </ul>"
        )
        frappe.throw(error_message)


def validate_job_applicant(submission):
    # TODO: add docField `allow_multiple_solutions` in `Job Test`
    if not submission.get("job_applicant"):
        frappe.throw("Invalid submission, no Job Applicant provided!")

    if frappe.db.get_value(
        "Aptitude Test Submission",
        filters={"job_applicant": submission["job_applicant"]},
    ):
        frappe.throw(
            "Test has already been submitted for {}. You're not allowed to take test again!".format(
                submission["job_applicant"]
            )
        )


def wrap_with_html_tag(string, tag):
    return f"<{tag}>{string}</{tag}>"
