# Copyright (c) 2021, Aakvatech Limited and contributors
# For license information, please see license.txt
import json

import frappe
from frappe.website.website_generator import WebsiteGenerator


class JobTest(WebsiteGenerator):
    website = frappe._dict(
        template="templates/generators/job_test.html",
        page_title_field="title",
    )

    def get_context(self, context):
        keys_to_include = {
            "name",
            "question",
            "required",
            "question_type",
            "options",
            "placeholder_text",
        }

        context.questions = [
            {key: question[key] for key in keys_to_include}
            for question in context.questions
        ]

        # for JavaScript
        context.questions_json = json.dumps(context.questions)
