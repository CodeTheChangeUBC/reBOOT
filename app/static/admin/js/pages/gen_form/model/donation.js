"use strict";
define(["../util/util"], function(util) {
    class Donation {
        constructor(data = {}) {
            this.donor_id = data.donor_id;
            this.tax_receipt_no = data.tax_receipt_no;
            this.donate_date = data.donate_date;
            this.pick_up = data.pick_up;
            this.verified = data.verified;
        }

        toJson() {
            return {
                donor_id: this.donor_id,
                tax_receipt_no: this.tax_receipt_no,
                donate_date: this.donate_date,
                pick_up: this.pick_up,
                verified: this.verified
            };
        }

        /**
         * Takes a success callback and saves the current donation
         * @param {Function} successFn
         */
        get(successFn = util.noop) {
            return util.ajax({
                url: "/api/donation",
                type: "POST",
                data: this.toJson(),
                success: successFn,
            });
        }

        /**
         * Takes a success callback and saves the current donation
         * @param {Function} successFn
         */
        save(successFn = util.noop) {
            return util.ajax({
                url: "/api/donation",
                type: "POST",
                data: this.toJson(),
                success: successFn,
            });
        }
        /**
         * Takes a success callback and updates the current donation
         * @param {Function} successFn
         */
        update(successFn = util.noop) {
            return util.ajax({
                url: "/api/donation",
                type: "PUT",
                data: this.toJson(),
                success: successFn,
            });
        }

        /**
         * Takes a success callback and updates the current donation
         * @param {Function} successFn
         */
        delete(successFn = util.noop) {
            return util.ajax({
                url: "/api/donation",
                type: "DELETE",
                data: {
                    tax_receipt_no: this.tax_receipt_no
                },
                success: successFn,
            });
        }
    }


    /**
     * Take a success callback and get related donations based on donor_id
     * @param {ID} id
     * @param {Function} successFn
     */
    Donation.getRelated = function(id, successFn = util.noop) {
        return util.ajax({
            url: "/api/related_donations",
            type: "GET",
            data: {
                donor_id: id
            },
            success: successFn,
        });
    };

    return Donation;
});
