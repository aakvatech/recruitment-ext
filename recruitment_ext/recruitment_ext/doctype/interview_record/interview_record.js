// Copyright (c) 2021, Aakvatech Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Interview Record', {
	refresh: function(frm) {
		if (!frm.doc.interviewer) {
			frm.set_value("interviewer", frappe.session.user_fullname)
		}
	},

	onload: function(frm){
		frm.set_total_benchmark_score = function(frm){
			var questn_list = frm.doc.questn_list;
			var total_bench_mark_score = 0;
			for (var i in questn_list) {
				total_bench_mark_score = total_bench_mark_score + questn_list[i].benchmark_score
			}
			frm.set_value("total_benchmark_score", total_bench_mark_score)
		}

		frm.validate_interview_score = function(frm, row) {
			frm.doc.questn_list.forEach(data=>{
				if (data.benchmark_score < data.interview_score) {
					row.interview_score = 0;
					msgprint(
						"Interview Score Can not be Greater than Benchmark Score..!!, \
						Please Make Sure Interview Score is Correct to Proceed..!!"
					)
					frm.refresh_field("questn_list")
				}
			})
		}

		frm.set_total_interview_score = function(frm) {
			let total = 0;
			frm.doc.questn_list.forEach(d=>{
				total = total + d.interview_score;
			})
			frm.set_value("total_interview_score", total)
		}
	}
});

frappe.ui.form.on("Interview Data", {
	interview_score: function(frm, cdt,cdn) {
		let row = locals[cdt][cdn];
		frm.validate_interview_score(frm, row, row.interview_score)
		frm.set_total_interview_score(frm)
	},
	benchmark_score: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		frm.set_total_benchmark_score(frm)
	}
})