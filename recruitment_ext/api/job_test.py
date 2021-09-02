import json

import frappe
from frappe import bold


@frappe.whitelist(allow_guest=True)
def submit_job_test(submission):
    submission = frappe._dict(json.loads(submission))
    questions = frappe.get_all(
        "Job Test Question",
        filters={"parent": submission["job_test"]},
        fields=["*"],
    )
    validate_submision(questions, submission)

    # TODO: Remove below line after fetching applicant from form
    submission["job_applicant"] = "Pruthvi Patel - pruthvi@resilient.tech"
    answers = get_answers(questions, submission)
    doc = frappe.get_doc(
        {
            "doctype": "Job Test Submission",
            "job_test": submission["job_test"],
            "job_applicant": submission["job_applicant"],
            "answers": answers,
            "earned_points": sum(ans["points"] for ans in answers),
        }
    )
    print(doc.as_dict())
    doc.save()
    return {}


def get_answers(questions, submission):
    answers = []
    for question in questions:
        answer = {
            "question": question.name,
            "points": 0,
        }

        if question.question_type == "Multi Select":
            answer["answer"] = "\n".join(
                map(
                    lambda option: option.strip(),
                    submission["answers"].get(question.name, []),
                )
            )
        else:
            answer["answer"] = submission["answers"].get(question.name, "")

        # calculate points
        if (
            question.correct_answer
            and question.question_type in ("MCQ", "Answer", "Multi Select")
            and question.correct_answer.strip() == answer["answer"].strip()
        ):
            answer["points"] = question.points

        answers.append(answer)
    return answers


def validate_submision(questions, submission):
    # TODO: uncomment below validation after getting applicant from form
    # validate_job_applicant(submission)
    error_message = ""

    for question in questions:
        # TODO: remove these 2 lines after adding fields to the doctype
        question.min_allowed_answer = 1
        question.max_allowed_answer = 3

        if question.required and not submission.answers.get(question.name):
            error_message += wrap_with_html_tag(
                f"The question: { bold(question.question) } is required!", "li"
            )

        if question.question_type != "Multi Select":
            continue

        number_of_answers = len(submission.answers.get(question.name, []))
        if not question.required and not number_of_answers:
            continue

        if number_of_answers < question.min_allowed_answer:
            error_message += wrap_with_html_tag(
                f"choose atleast { bold(question.min_allowed_answer) } option(s) for the question: { bold(question.question) }",
                "li",
            )
        if number_of_answers > question.max_allowed_answer:
            error_message += wrap_with_html_tag(
                f"maximum { bold(question.max_allowed_answer) } option(s) allowed to choose for the question: { bold(question.question) }",
                "li",
            )

    if error_message:
        error_message = (
            f"Following Questions have errors: <br><br><ul> {error_message} </ul>"
        )
        frappe.throw(error_message)


def validate_job_applicant(submission):

    if not submission.get("job_applicant"):
        frappe.throw("Invalid submission, no Job Applicant provided!")

    if frappe.db.get_value(
        "Job Test Submission", filters={"job_applicant": submission["job_applicant"]}
    ):
        frappe.throw(
            "Test has already been submitted for {}. You're not allowed to take test again!".format(
                submission["job_applicant"]
            )
        )


def wrap_with_html_tag(string, tag):
    return f"<{tag}>{string}</{tag}>"
