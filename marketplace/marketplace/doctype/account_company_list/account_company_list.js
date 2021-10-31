// Copyright (c) 2021, Marketplace and contributors
// For license information, please see license.txt

frappe.ui.form.on('Account Company List', {
	validate: function(frm) {
		let str = cur_frm.doc.account_head;
		let substrings = str.split('-');
		frm.set_value('description',substrings[1])
		console.log(substrings[1])
		let str2 = cur_frm.doc.diskon_account;
		let substrings2 = str2.split('-');
		frm.set_value('description_disc',substrings2[1])
		console.log(substrings2[1])
	}
});
