define([], function () {
    /**
     * Donor form fields
     */
    var dom = {
        button: {
            delete  : document.getElementById("btn_delete_donor"),
            save    : document.getElementById("btn_save_donor"),
            update  : document.getElementById("btn_update_donor")
        },
        input: {
            id      : document.getElementById("id_donor_id"),
            name    : document.getElementById("id_donor_name"),
            email   : document.getElementById("id_email"),
            telephone: document.getElementById("id_telephone_number"),
            mobile  : document.getElementById("id_mobile_number"),
            ref     : document.getElementById("id_customer_ref"),
            needReceipt: document.getElementById("id_want_receipt"),
            address : document.getElementById("id_address_line"),
            city    : document.getElementById("id_city"),
            province: document.getElementById("id_province"),
            postalCode: document.getElementById("id_postal_code")
        },
        form: document.getElementById("donor_form")
    };

    return dom;
}.bind({}));
// QUESTION: Is this .bind necessary? Couldn't we just return normal object back?
// If we were to global state variable for donor view, that might be a thought but this isn't what this does.
