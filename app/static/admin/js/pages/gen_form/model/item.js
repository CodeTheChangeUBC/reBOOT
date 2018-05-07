define(["../util/util", "../view/item"], function (util, dom) {

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
            dom.div.itemId.hidden = true;
            util.setButton(dom.button, "new");
            util.scrollTo(dom.input.description);
            dom.input.taxReceiptNo.value = store.tax_receipt_no;

            return;
        }

        if (this == dom.button.cancel) {
            util.emptyAllFields(dom.input);
            dom.div.form.hidden = true;
            util.setButton(dom.button, null);

            return;
        }

        dom.input.taxReceiptNo.value = data.tax_receipt_no_id;
        dom.input.itemId.value = data.id;
        dom.input.description.value = data.description;
        dom.input.particulars.value = data.particulars;
        dom.input.manufacturer.value = data.manufacturer;
        dom.input.model.value = data.model;
        dom.input.quantity.value = data.quantity;
        dom.input.isWorking.checked = data.isWorking;
        dom.input.condition.value = data.condition;
        dom.input.quality.value = data.quality;
        dom.input.isVerified.checked = data.verified;
        dom.input.batch.value = data.batch;
        dom.input.value.value = data.value;

        dom.div.form.hidden = false;
        dom.div.itemId.hidden = false;
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

            for (var ix = 0, ixLen = data.length; ix < ixLen; ix++) {
                item = data[ix];
                store[item.id] = item;
                html +=
                    '<tr class="row' +
                    (ix % 2 ? 2 : 1) +
                    '" id="' +
                    item.id +
                    '" >\n' +
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

    var callback = {
        post: {
            success: function(response) {
                alert('New item saved. [id: ' + arguments[0].id + ']' );
                getItems.call({id: dom.input.taxReceiptNo.value});
            },
            fail: util.somethingWentWrong
        },
        get: {
            success: printItemList,
            fail: util.somethingWentWrong
        },
        put: {
            success: function() {
                alert('Item updated. [id: ' + arguments[0].id + ']' );
                getItems.call({id: dom.input.taxReceiptNo.value});
            },
            fail: util.somethingWentWrong
        },
        delete: {
            success: function() {
                alert('Deleted.');
                getItems.call({id: dom.input.taxReceiptNo.value});
            },
            fail: util.somethingWentWrong
        }
    };

    var store = {};
    function getItems() {
        store = {};
        store.tax_receipt_no = this.id;

        util.ajax({
            url: "/api/item",
            type: "GET",
            data: { tax_receipt_no: this.id },
            success: callback.get.success,
            error: callback.get.fail
        });
    }

    function saveItem() {
        util.ajax({
            url: "/api/item",
            type: "POST",
            data: $(dom.form).serialize(),
            success: callback.post.success,
            error: callback.post.fail
        });
    }

    var updateItem = function() {
        util.ajax({
            url: "/api/item",
            type: "PUT",
            data: $(dom.form).serialize(),
            success: callback.put.success,
            error: callback.put.fail
        });
    };

    var deleteItem = function() {
        util.ajax({
            url: "/api/item",
            type: "DELETE",
            data: { item_id: dom.input.itemId.value },
            success: callback.delete.success,
            error: callback.delete.fail
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
        clearItemView: printItemList,
        getItems: getItems
    };
}.bind({}));
