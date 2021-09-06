frappe.ready(() => {
    frappe.web_form.handle_success = () => {};
    frappe.web_form.events.on("after_save", () => {
        window.location.assign("http://aptitude-test.localhost:8004/aptitude_test?job_applicant=Test%20Applicant%20Name%20-%20test@example.com%20-%20sales-representative&job_opening=sales-representative")
    })
})

