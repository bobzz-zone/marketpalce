// Copyright (c) 2021, Marketplace and contributors
// For license information, please see license.txt

frappe.ui.form.on('Marketplace Invoice', {
	validate: function(frm) {
        //frappe.msgprint('before_save')
        let data = cur_frm.doc.marketplace_order.length;
        let data2 = cur_frm.doc.marketplace_order;
        let total_disc = 0;
        let sum = []
        for (let i = 0; i < data; i++) {
            sum.push(data2[i].qty * data2[i].diskon)
        }
        for (let j = 0; j < sum.length; j++) {
            total_disc += sum[j];
        }
        //console.log(total_disc)
        frm.set_value("total_diskon",total_disc);
        //frm.save(); 
	},
    refresh: function(frm) {
        if(cur_frm.doc.sinv){
            frm.set_df_property('ongkir', 'read_only',!frm.is_new());
            frm.set_df_property('date', 'read_only',!frm.is_new());
            frm.set_df_property('customer', 'read_only',!frm.is_new());
            frm.set_df_property('customer_real', 'read_only',!frm.is_new());
            frm.set_df_property('alamat', 'read_only',!frm.is_new());
            frm.set_df_property('no_telp', 'read_only',!frm.is_new());
            frm.set_df_property('order_id', 'read_only',!frm.is_new());
            frm.set_df_property('invoice_id', 'read_only',!frm.is_new());
            frm.set_df_property('marketplace_order', 'read_only',!frm.is_new());
            frm.set_df_property('company', 'read_only',!frm.is_new());
        }
        if(cur_frm.doc.naming_series == 'MINV-BBO.YY.MM.#####'){
            frm.set_value('company','BB ONLINE') 
        }
        if(cur_frm.doc.naming_series == 'MINV-BMO.YY.MM.#####'){
            frm.set_value('company','BM ONLINE') 
        }
    }
});

frappe.ui.form.on("Marketplace Invoice", "naming_series", function(frm) {
    if(cur_frm.doc.naming_series == 'MINV-BBO.YY.MM.#####'){
            frm.set_value('company','BB ONLINE') 
        }
    if(cur_frm.doc.naming_series == 'MINV-BMO.YY.MM.#####'){
        frm.set_value('company','BM ONLINE') 
    }
})


/*frappe.ui.form.on("Marketplace Order", "rate", function(frm, cdt, cdn) {
    var item = locals[cdt][cdn];
    var result = item.qty*rate;
    item.total = result;
});*/



frappe.ui.form.on('Marketplace Order', {
    rate: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if(row.rate && !row.diskon){
            //frappe.msgprint("Harga")
            frappe.model.set_value(cdt, cdn, 'total', row.qty*row.rate);
        }
    },
    diskon: function (frm, cdt, cdn) {
        var row2 = locals[cdt][cdn];
        if(row2.diskon && row2.rate){
            //frappe.msgprint("Diskon")
            var harga = row2.qty*row2.rate
            var disc = row2.qty*row2.diskon
            var total = harga - disc
            frappe.model.set_value(cdt, cdn, 'total', total);
        }
    },
    qty: function (frm, cdt, cdn) {
        var row3 = locals[cdt][cdn];
        if(row3.qty){
            //frappe.msgprint("Diskon")
            var harga = row3.qty*row3.rate
            var disc = row3.qty*row3.diskon
            var total = harga - disc
            frappe.model.set_value(cdt, cdn, 'total', total);
        }
    }

});

/*frappe.ui.form.on('Marketplace Order', {
    refresh(frm) {
        // your code here
        var row = locals[cdt][cdn];
        if(row.item_code){
            frappe.msgprint("diskon")
        }
    }
})*/