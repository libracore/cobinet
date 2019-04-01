// Copyright (c) 2019, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('Preisangebot', {
	refresh: function(frm) {

	},
    item: function(frm) {
        update_title(frm);
    },
    supplier: function(frm) {
        update_title(frm);
    }
});

function update_title(frm) {
    if ((frm.doc.item) && (frm.doc.supplier)) {
        cur_frm.set_value('title', frm.doc.item + " - " + frm.doc.supplier);
    }
}
