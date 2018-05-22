"use strict";
define([], function() {
    /**
     * Donor form fields
     */
    var dom = {
        form: document.getElementById("donor_form"),
        button: {
            delete: document.getElementById("btn_delete_donor"),
            save: document.getElementById("btn_save_donor"),
            update: document.getElementById("btn_update_donor")
        },
        input: {
            id: document.getElementById("id_donor_id"),
            donorName: document.getElementById("id_donor_name"),
            email: document.getElementById("id_email"),
            telephoneNumber: document.getElementById("id_telephone_number"),
            mobileNumber: document.getElementById("id_mobile_number"),
            customerRef: document.getElementById("id_customer_ref"),
            wantReceipt: document.getElementById("id_want_receipt"),
            addressLine: document.getElementById("id_address_line"),
            city: document.getElementById("id_city"),
            province: document.getElementById("id_province"),
            postalCode: document.getElementById("id_postal_code")
        }
    };

    return dom;
});
