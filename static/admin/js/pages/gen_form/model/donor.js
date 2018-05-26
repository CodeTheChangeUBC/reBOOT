"use strict";
define(["../util/util"], function(util) {
    class Donor {
        constructor(data = {}) {
            this.id = data.id;
            this.donorName = data.donorName;
            this.email = data.email;
            this.telephoneNumber = data.telephoneNumber;
            this.mobileNumber = data.mobileNumber;
            this.customerRef = data.customerRef;
            this.wantReceipt = data.wantReceipt;
            this.addressLine = data.addressLine;
            this.city = data.city;
            this.province = data.province;
            this.postalCode = data.postalCode;
        }

        toJson() {
            return {
                id: this.id,
                donorName: this.donorName,
                email: this.email,
                telephoneNumber: this.telephoneNumber,
                mobileNumber: this.mobileNumber,
                customerRef: this.customerRef,
                wantReceipt: this.wantReceipt,
                addressLine: this.addressLine,
                city: this.city,
                province: this.province,
                postalCode: this.postalCode
            };
        }

        uniqueName() {
            return this.donorName + ", " + this.id;
        }

        /**
         * Takes a success callback and saves the current donor
         * @param {Function} successFn
         */
        save(successFn = util.noop) {
            return util.ajax({
                url: "/api/donor",
                type: "POST",
                data: this.toJson(),
                success: successFn,
            });
        }
        /**
         * Takes a success callback and updates the current donor
         * @param {Function} successFn
         */
        update(successFn = util.noop) {
            return util.ajax({
                url: "/api/donor",
                type: "PUT",
                data: this.toJson(),
                success: successFn,
            });
        }

        /**
         * Takes a success callback and updates the current donor
         * @param {Function} successFn
         */
        delete(successFn = util.noop) {
            return util.ajax({
                url: "/api/donor",
                type: "DELETE",
                data: {
                    id: this.id
                },
                success: successFn,
            });
        }
    }
    // Class methods

    /**
     * Takes a success callback and data respond with array of serialized donor info
     * @param {String} data
     * @param {Function} successFn
     */
    Donor.autocomplete = function(data, successFn) {
        util.ajax({
            type: "GET",
            url: "/api/autocomplete_name",
            data: {
                key: data
            },
            success: successFn,
        });
    };

    return Donor;
});
