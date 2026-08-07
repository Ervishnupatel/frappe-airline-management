// Copyright (c) 2026, xzy and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        frm.add_custom_button(__("Assign Seat"), () => {
            let dialog = new frappe.ui.Dialog({
                title: __("Assign Seat"),
                fields: [
                    {
                        label: __("Seat"),
                        fieldname: "seat",
                        fieldtype: "Data",
                        reqd: 1
                    }
                ],
                primary_action_label: __("Assign"),
                primary_action(values) {
                    frm.set_value("seat", values.seat);
                    dialog.hide();
                }
            });

            dialog.show();
        });
    }
});