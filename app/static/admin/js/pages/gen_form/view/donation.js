"use strict";
define([], function() {
    /**
     * Donation table & form fields
     */
    var dom = {
        div: {
            header: document.getElementById("donation_header"),
            form: document.getElementById("donation_form"),
            taxReceiptNo: document
                .getElementById("donation_form")
                .getElementsByClassName("field-tax_receipt_no")[0]
        },
        form: $(
            document.getElementById("donation_form").getElementsByTagName("form")[0]
        ),
        table: {
            tbody: document
                .getElementById("donation_result_list")
                .getElementsByTagName("tbody")[0]
        },
        button: {
            delete: document.getElementById("btn_delete_donation"),
            save: document.getElementById("btn_save_donation"),
            update: document.getElementById("btn_update_donation"),
            addNew: document.getElementById("btn_add_new_donation"),
            cancel: document.getElementById("btn_cancel_donation")
        },
        input: {
            donorId: document.getElementById("id_donation_donor"),
            taxReceiptNo: document.getElementById("id_tax_receipt_no"),
            date: document.getElementById("id_donate_date"),
            isVerified: document.getElementById("id_verified"),
            pickUpPostalCode: document.getElementById("id_pick_up")
        }
    };

    return dom;
});
