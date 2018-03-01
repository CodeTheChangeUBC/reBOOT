define(["./form-util"], function (util) {
    /**
     * Items table & form fields
     */
    var dom = {
        div: {
            container: document.getElementById("item_container"),
            header: document.getElementById("item_header"),
            form: document.getElementById("item_form")
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

    var setItemForm = function (data) {
            // [*]
            if (this == dom.button.addNew && !util.isDonorNamePresent) {
                util.enterDonorName();
                return;
            }

            if (!data) {
                util.emptyAllFields(dom.input);
                dom.div.form.hidden = true;
                util.setButton(dom.button, null);

                return;
            }

            if (this == dom.button.cancel) {
                util.emptyAllFields(dom.input);
                dom.div.form.hidden = true;
                util.setButton(dom.button, null);

                return;
            }

            if (this == dom.button.addNew) {
                util.emptyAllFields(dom.input);
                dom.div.form.hidden = false;
                util.setButton(dom.button, "new");
                util.scrollTo(dom.input.description);

                return;
            }

            if (this == dom.button.cancel) {
                util.emptyAllFields(dom.input);
                dom.div.form.hidden = true;
                util.setButton(dom.button, null);

                return;
            }

            // TODO item id
            dom.input.taxReceiptNo.value = data.taxReceiptNo;
            dom.input.itemId.value = data.id;
            dom.input.description.value = data.description;
            dom.input.particulars.value = data.particulars;
            dom.input.manufacturer.value = data.manufacturer;
            dom.input.model.value = data.model;
            dom.input.quantity.value = data.quantity;
            dom.input.isWorking.checked = data.isWorking;
            dom.input.condition.value = data.condition;
            dom.input.quality.value = data.quality;
            dom.input.isVerified.checked = data.isVerified;
            dom.input.batch.value = data.batch;
            dom.input.value.value = data.value;

            dom.div.form.hidden = false;
            util.setButton(dom.button, "existing");
    };


    var store;
    var printItemList = function () {
        var _this = this;

        return function (data) {
            if (!data) {
                _this.div.container.hidden = true;
                setItemForm(null);
                return;
            }

            _this.div.container.hidden = false;
            _this.div.header.value = this.id; // tax_receipt_no;

            var html = "";
            var item;
            store = {};

            for (var ix = 0, ixLen = data.length; ix < ixLen; ix++) {
                item = data[ix];
                store[item.id] = item;
                html +=
                    '<tr class="row' +
                    (ix % 2 ? 2 : 1) +
                    '" id="' +
                    item.id +
                    '" >\n' +
                    // '                        <td class="action-checkbox"><input type="checkbox" name="_selected_action" value='+item.item_id +'\n' +
                    // '                                                           class="action-select"></td>\n' +
                    '<td class="field-get_item">' +
                    item.id +
                    "</td>\n" +
                    '<td class="field-manufacturer">' +
                    item.manufacturer +
                    "</td>\n" +
                    '<td class="field-model">' +
                    item.model +
                    "</td>\n" +
                    '<td class="field-quantity">' +
                    item.quantity +
                    "</td>\n" +
                    '<td class="field-batch">' +
                    item.batch +
                    "</td>\n" +
                    '<td class="field-verified">' +
                    (item.verified
                        ? '<img src="/static/admin/img/icon-yes.svg" alt=true>'
                        : '<img src="/static/admin/img/icon-no.svg" alt=false>') +
                    "</td>\n" +
                    "</tr>";
            }

            setItemForm(null);
            util.setButton(_this.button, null);
            _this.table.tbody.innerHTML = html;
        };
    }.call(dom);

    var getItems = function () {
        $.ajax({
            beforeSend: util.csrf,
            url: "/api/item",
            type: "GET",
            dataType: "json",
            data: {
                tax_receipt_no: this.id
            },
            success: printItemList,
            error: function () {
                console.error(arguments);
            }
        });
    };

    var saveItem = function() {
        $.ajax({
            beforeSend: util.csrf,
            url: "/api/item",
            type: "POST",
            dataType: "json",
            data: $(dom.form).serialize(),
            success: getItems.bind({ id: dom.form.taxReceiptNo.value }),
            error: function () {
                console.error(arguments);
            }
        });
    };

    var updateItem = function() {
        $.ajax({
            beforeSend: util.csrf,
            url: "/api/item",
            type: "PUT",
            dataType: "json",
            data: $(dom.form).serialize(),
            success: getItems.bind({ id: dom.input.taxReceiptNo.value }),
            error: function () {
                console.error(arguments);
            }
        });
    };

    var deleteItem = function() {
        $.ajax({
            beforeSend: util.csrf,
            url: "/api/item",
            type: "DELETE",
            dataType: "json",
            data: { item_id: dom.input.itemId.value },
            success: getItems.bind({ id: dom.input.taxReceiptNo.value }),
            error: function () {
                console.error(arguments);
            }
        });
    };

    $(dom.table.tbody).on("click", "tr", function (e) {
        setItemForm(store[this.id]);
        scrollTo(this);
    });

    $(dom.button.addNew).on("click", setItemForm);
    $(dom.button.cancel).on("click", setItemForm);
    $(dom.button.save).on("click", saveItem);
    $(dom.button.update).on("click", updateItem);
    $(dom.button.delete).on("click", deleteItem);


    return {
        clearItemList: printItemList,
        getItems: getItems
    };
}.bind({}));
