"use strict";
define(["../util/util"], function(util) {
    class Donor {
        constructor(data = {}) {
            this.id = data.id;
            this.donor_name = data.donor_name;
            this.email = data.email;
            this.telephone_number = data.telephone_number;
            this.mobile_number = data.mobile_number;
            this.customer_ref = data.customer_ref;
            this.want_receipt = data.want_receipt;
            this.address_line = data.address_line;
            this.city = data.city;
            this.province = data.province;
            this.postal_code = data.postal_code;
            this.donations = data.donations || [];
        }

        toJson() {
            return {
                id: this.id,
                donor_name: this.donor_name,
                email: this.email,
                telephone_number: this.telephone_number,
                mobile_number: this.mobile_number,
                customer_ref: this.customer_ref,
                want_receipt: this.want_receipt,
                address_line: this.address_line,
                city: this.city,
                province: this.province,
                postal_code: this.postal_code
            };
        }

        uniqueName() {
            return this.donor_name + ", " + this.id;
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
