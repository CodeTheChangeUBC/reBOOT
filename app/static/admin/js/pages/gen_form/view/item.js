define([], function () {
    /**
     * Items table & form fields
     */
    var dom = {
        div: {
            container: document.getElementById("item_container"),
            header: document.getElementById("item_header"),
            form: document.getElementById("item_form"),
            itemId: document
                .getElementById("item_form")
                .getElementsByClassName("field-tax_receipt_no")[0]
        },
        table: {
            tbody: document
                .getElementById("item_result_list")
                .getElementsByTagName("tbody")[0]
        },
        button: {
            delete: document.getElementById("btn_delete_item"),
            save: document.getElementById("btn_save_item"),
            update: document.getElementById("btn_update_item"),
            addNew: document.getElementById("btn_add_new_item"),
            cancel: document.getElementById("btn_cancel_item")
        },
        input: {
            taxReceiptNo: document.getElementById("id_tax_receipt_no_for_item"),
            itemId: document.getElementById("id_item_id"),
            description: document.getElementById("id_description"),
            particulars: document.getElementById("id_particulars"),
            manufacturer: document.getElementById("id_manufacturer"),
            model: document.getElementById("id_model"),
            quantity: document.getElementById("id_quantity"),
            isWorking: document.getElementById("id_working"),
            condition: document.getElementById("id_condition"),
            quality: document.getElementById("id_quality"),
            isVerified: document.getElementById("id_item_verified"),
            batch: document.getElementById("id_batch"),
            value: document.getElementById("id_value")
        },
        form: document.getElementById("item_form")
    };

    return dom;
}.bind({}));
