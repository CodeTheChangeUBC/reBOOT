"use strict";
define(["../util/util"], function(util) {
    class Item {
        constructor(data = {}) {
            this.tax_receipt_no = data.tax_receipt_no;
            this.id = data.id;
            this.description = data.description;
            this.particulars = data.particulars;
            this.manufacturer = data.manufacturer;
            this.model = data.model;
            this.quantity = data.quantity;
            this.working = data.working;
            this.condition = data.condition;
            this.quality = data.quality;
            this.batch = data.batch;
            this.value = data.value;
            this.verified = data.verified;
        }

        toJson() {
            return {
                tax_receipt_no: this.tax_receipt_no,
                id: this.id,
                description: this.description,
                particulars: this.particulars,
                manufacturer: this.pickmanufacturerUp,
                model: this.model,
                quantity: this.quantity,
                working: this.working,
                condition: this.condition,
                quality: this.quality,
                batch: this.batch,
                value: this.value,
                verified: this.verified
            };
        }

        /**
         * Takes a success callback and id and get related item
         * @param {ID} id
         * @param {Function} successFn
         */
        get(id, successFn = util.noop) {
            return util.ajax({
                url: "/api/item",
                type: "GET",
                data: {
                    id: id
                },
                success: successFn,
            });
        }

        /**
         * Takes a success callback and saves the current item
         * @param {Function} successFn
         */
        save(successFn = util.noop) {
            return util.ajax({
                url: "/api/item",
                type: "POST",
                data: this.toJson(),
                success: successFn,
            });
        }
        /**
         * Takes a success callback and updates the current item
         * @param {Function} successFn
         */
        update(successFn = util.noop) {
            return util.ajax({
                url: "/api/item",
                type: "PUT",
                data: this.toJson(),
                success: successFn,
            });
        }

        /**
         * Takes a success callback and updates the current item
         * @param {Function} successFn
         */
        delete(successFn = util.noop) {
            return util.ajax({
                url: "/api/item",
                type: "DELETE",
                data: {
                    id: this.id
                },
                success: successFn,
            });
        }
    }


    /**
     * Take a success callback and get related items based on tax_receipt_no
     * @param {ID} id
     * @param {Function} successFn
     */
    Item.getRelated = function(id, successFn = util.noop) {
        return util.ajax({
            url: "/api/related_items",
            type: "GET",
            data: {
                donorId: id
            },
            success: successFn,
        });
    };

    return Item;
});
