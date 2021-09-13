// Copyright (c) 2021, Aakvatech Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Aptitude Test', {
	total_earned_points(frm) {
		if (!frm.doc.total_points) return;
		frm.set_value("result_percentage", flt(frm.doc.total_earned_points / frm.doc.total_points * 100, 2));
	},
});

frappe.ui.form.on('Aptitude Test Answer', {
	earned_points(frm, cdt, cdn) {
		validate_earned_points(frappe.get_doc(cdt, cdn));
		calculate_total_earned_points(frm);
	}
});

function validate_earned_points(row) {
	if (row.earned_points > row.max_points) {
		frappe.throw(`<b>Earned Points(${row.earned_points})</b> can not be greater than <b>Points(${row.max_points})</b>`);
	}
}

function calculate_total_earned_points(frm) {
	const total_earned_points = frm.doc.answers.reduce(
		(sum, answer) => sum + answer.earned_points, 0
	);
	frm.set_value("total_earned_points", total_earned_points);
}

