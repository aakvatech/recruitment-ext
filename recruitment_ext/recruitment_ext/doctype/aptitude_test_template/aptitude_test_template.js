// Copyright (c) 2021, Aakvatech Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Aptitude Test Template', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Aptitude Test Question', {
	points(frm) {
		const total_points = frm.doc.questions.reduce((sum, question) =>
			sum + (question.question ? question.points : 0)
			, 0);
		frm.set_value("total_points", total_points);
	}
});
