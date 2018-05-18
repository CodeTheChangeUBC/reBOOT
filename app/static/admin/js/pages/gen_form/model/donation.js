"use strict";
define(["../util/util"], function(util) {
    class Donation {
        constructor(data = {}) {
            this.donorId = data.donorIdId;
            this.taxReceiptNo = data.taxReceiptNo;
            this.donateDate = data.donateDate;
            this.pickUp = data.pickUp;
            this.verified = data.verified;
        }

        toJson() {
            return {
                donorId: this.donorId,
                taxReceiptNo: this.taxReceiptNo,
                donateDate: this.donateDate,
                pickUp: this.pickUp,
                verified: this.verified
            };
        }

        /**
         * Takes a success callback and taxReceiptNo and get related donation
         * @param {String} taxReceiptNo
         * @param {Function} successFn
         */
        get(taxReceiptNo, successFn = util.noop) {
            return util.ajax({
                url: "/api/donation",
                type: "GET",
                data: {
                    taxReceiptNo: taxReceiptNo
                },
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
                    taxReceiptNo: this.taxReceiptNo
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
                donorId: id
            },
            success: successFn,
        });
    };

    return Donation;
});
