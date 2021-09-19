import json

import frappe
from frappe import bold


CONTACT_MSG = "<br><br>If this seems like a mistake, please email us for support."


def get_context(context):
    validate_query_params()
    job_opening = frappe.get_doc("Job Opening", frappe.form_dict["job_opening"])
    if not job_opening.get("aptitude_test_template"):
        return

    aptitude_test = frappe.get_doc("Aptitude Test Template", job_opening.aptitude_test_template)

    # if Aptitude test is already submitted for given Applicant, show success message (handled in js)
    if frappe.db.get_value(
        "Aptitude Test",
        filters={"job_applicant": frappe.form_dict["job_applicant"]},
    ):
        context["has_submitted"] = 1

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
            "doctype": "Aptitude Test",
            "aptitude_test": submission["aptitude_test"],
            "job_applicant": submission["job_applicant"],
            "answers": answers,
        }
    )
    doc.flags.ignore_permissions = True
    doc.submit()


@frappe.whitelist(allow_guest=True)
def get_aptitude_test(job_opening):
    return frappe.db.get_value("Job Opening", job_opening, "aptitude_test_template")


def validate_query_params():
    for key in ("job_opening", "job_applicant"):
        if not frappe.form_dict.get(key):
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
    def wrap_with_html_tag(string, tag):
        return f"<{tag}>{string}</{tag}>"

    error_message = ""
    for question in questions:
        if question.required and not submission.answers.get(question.name):
            error_message += wrap_with_html_tag(
                f"The question: { bold(question.question) } is required!", "li"
            )

        if question.question_type != "MCQ - Multiple Answers" or not question.required:
            continue

        number_of_answers = len(submission.answers.get(question.name, []))

        if number_of_answers < question.min_allowed_answers:
            error_message += wrap_with_html_tag(
                f"choose atleast { bold(question.min_allowed_answers) } option(s) for the question: { bold(question.question) }",
                "li",
            )
        elif number_of_answers > question.max_allowed_answers:
            error_message += wrap_with_html_tag(
                f"maximum { bold(question.max_allowed_answers) } option(s) allowed to choose for the question: { bold(question.question) }",
                "li",
            )

    if error_message:
        error_message = (
            f"Following Questions have errors: <br><br><ul> {error_message} </ul>"
        )
        frappe.throw(error_message)
