// Copyright (c) 2021, Marketplace and contributors
// For license information, please see license.txt

frappe.ui.form.on('Setting Account', {
	refresh: function(frm) {
		let str = cur_frm.doc.account_head;
		let substrings = str.split('-');
		frm.set_value('description',substrings[1])
		console.log(substrings[1])
	}
});
