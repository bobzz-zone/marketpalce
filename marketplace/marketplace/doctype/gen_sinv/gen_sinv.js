// Copyright (c) 2021, Marketplace and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gen Sinv', {
	refresh: function(frm) {
		cur_frm.cscript.generate_sinv = function(doc) {
			frappe.call({
	            method: "marketplace.marketplace.sinv_market.gen_invoice",
	            args: {
                    	tanggal: cur_frm.doc.date,
                    	com: cur_frm.doc.company
                }, callback: function(r) {}
	        });
		}
	}
});
