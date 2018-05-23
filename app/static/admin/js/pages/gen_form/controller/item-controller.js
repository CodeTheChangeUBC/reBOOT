"use strict";
define(["../util/util", "../view/item", "../model/item"], function(util, dom, Item) {

    var currentTaxReceiptNo;
    var currentItem = new Item();
    var items = {};

    var callback = {
        related: {
            success: function(response) {
                items = {};
                for (var i = 0; response && i < response.length; i++) {
                    var itemData = response[i];
                    itemData.taxReceiptNo = currentTaxReceiptNo;
                    items[itemData.id] = new Item(itemData);
                }
                printItemList(items);
            }
        },
        post: {
            success: function(response) {
                response.taxReceiptNo = currentTaxReceiptNo;
                currentItem = new Item(response);
                items[currentItem.id] = currentItem;
                alert('New item saved. [ID: ' + currentItem.id + ']');
                printItemList(items);
            },
        },
        put: {
            success: function(response) {
                response.taxReceiptNo = currentTaxReceiptNo;
                currentItem = new Item(response);
                items[currentItem.id] = currentItem;
                alert('Item updated. [ID: ' + currentItem.id + ']');
                printItemList(items);
            }
        },
        delete: {
            success: function() {
                var tempItemId = currentItem.id;
                delete items[tempItemId];
                alert('Item deleted. [ID: ' + tempItemId + ']');
                printItemList(items);
            }
        }
    };

    function addNewItemAction() {
        if (!util.isDonorNamePresent()) {
            util.enterDonorName();
            return;
        }
        util.emptyAllFields(dom.input);
        dom.div.form.hidden = false;
        dom.div.itemId.hidden = true;
        util.setButton(dom.button, "new");
        util.scrollTo(dom.input.description);
        dom.input.taxReceiptNo.value = currentTaxReceiptNo;
    }

    function setItemForm(data) {
        if (!data) {
            clearItemForm();
            return;
        }

        currentItem = data;
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
        dom.input.isVerified.checked = data.verified;
        dom.input.batch.value = data.batch;
        dom.input.value.value = data.value;

        dom.div.form.hidden = false;
        dom.div.itemId.hidden = false;
        util.setButton(dom.button, "existing");
    }

    function clearItemView() {
        dom.div.container.hidden = true;
        setItemForm(null);
    }

    function printItemList(data = {}) {
        if (!data || $.isEmptyObject(data)) {
            clearItemView();
            return;
        }

        dom.div.container.hidden = false;
        dom.div.header.value = dom.id; // tax_receipt_no;

        var html = "";
        var count = 0;

        $.each(data, function(key, item) {
            html += formatHtml(item, count);
            count++;
        });

        setItemForm(null);
        util.setButton(dom.button, null);
        dom.table.tbody.innerHTML = html;
    }

    function clearItemForm() {
        util.emptyAllFields(dom.input);
        dom.div.form.hidden = true;
        util.setButton(dom.button, null);
    }

    function formatHtml(item, count) {
        var rowId = (count % 2 ? 2 : 1);
        return '<tr class="row' + rowId + '">' +
            '<td class="field-get_item">' + item.id + '</td>\n' +
            '<td class="field-manufacturer">' + item.manufacturer + '</td>\n' +
            '<td class="field-model">' + item.model + "</td>\n" +
            '<td class="field-quantity">' + item.quantity + "</td>\n" +
            '<td class="field-batch">' + item.batch + "</td>\n" +
            '<td class="field-verified">' +
            (item.verified ?
                '<img src="/static/admin/img/icon-yes.svg" alt=true>' :
                '<img src="/static/admin/img/icon-no.svg" alt=false>') +
            "</td>\n" +
            "</tr>";
    }

    function getItems(taxReceiptNo) {
        currentTaxReceiptNo = taxReceiptNo;
        return Item.getRelated(currentTaxReceiptNo, callback.related.success);
    }

    function saveItem() {
        currentItem = new Item(util.serializeObject(dom.form));
        currentItem.save(callback.post.success);
    }

    function updateItem() {
        currentItem = new Item(util.serializeObject(dom.form));
        currentItem.update(callback.put.success);
    }

    function deleteItem() {
        currentItem.delete(callback.delete.success);
    }

    function isSameAsCurrent(id) {
        return currentItem.id === parseInt(id, 10);
    }

    $(dom.table.tbody).on("click", "tr", function() {
        var tr = this.children;
        var itemId = tr[0].innerText;

        if (isSameAsCurrent(itemId)) {
            clearItemForm();
        }

        setItemForm(items[itemId]);
        scrollTo(this);
    });

    $(dom.button.addNew).on("click", addNewItemAction);
    $(dom.button.cancel).on("click", clearItemForm);
    $(dom.button.save).on("click", saveItem);
    $(dom.button.update).on("click", updateItem);
    $(dom.button.delete).on("click", deleteItem);

    return {
        clearItemView: clearItemView,
        getItems: getItems
    };
});
