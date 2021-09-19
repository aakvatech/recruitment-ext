from . import __version__ as app_version

app_name = "recruitment_ext"
app_title = "Recruitment Ext"
app_publisher = "Aakvatech Limited"
app_description = "Recruitment Extenstion for ERPNext"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@aakvatech.com"
app_license = "MIT"
after_install = "recruitment_ext.install.after_install"

webform_include_js = {
    "Job Applicant": "scripts/web/job_application.js",
}

override_doctype_dashboards = {
    "Job Applicant": "recruitment_ext.api.job_applicant_dashboard.get_data",
}


