// Copyright (c) 2021, Aakvatech Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Interview Record', {
	refresh: function(frm) {
		if (!frm.doc.interviewer) {
			frm.set_value("interviewer", frappe.session.user_fullname)
		}
		
		set_total_interview_score(frm)
	}
});

let set_total_interview_score = function(frm) {
	var list = frm.doc.questn_list
	var total = 0
	for (var i in list) {
		total = total + list[i].interview_score
	}
	frm.set_value("total_interview_score", total)
	refresh_field("total_interview_score");
};




