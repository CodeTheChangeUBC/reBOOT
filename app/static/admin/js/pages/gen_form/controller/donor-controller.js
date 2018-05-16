"use strict";
define(["../util/util", "../model/donation", "../view/donor-view", "../model/donor"], function(util, donation, dom, Donor) {

    var donor = new Donor();
    // QUESTION: What is this store for? Is it for caching variables? Seems to be some sort of storage for API call store.
    var store = {};


    var callback = {
        post: {
            success: function(donorData) {
                donor = new Donor(donorData);
                alert(donor.donor_name + ' saved.');
                // store = {};
                // QUESTION: camelCase these.
                // var str = donor.donor_name + ', ' + donor.id;
                store[donor.uniqueName()] = donor;
                dom.input.name.value = donor.uniqueName();
                setDonorForm(store[donor.uniqueName()]);
            }
        },
        put: {
            success: function(donor) {
                alert(donor.donor_name + ' updated.');
                store = {};
                var str = donor.donor_name + ', ' + donor.id;
                store[str] = donor;
                dom.input.name.value = str;
            }
        },
        get: {
            success: function(data) {
                store = {};
                data.reduce(function(store, donor) {
                    var str = donor.donor_name + ', ' + donor.id;
                    store[str] = donor;
                    return store;
                }, store);

                // Requires binding to response from autocomplete in order to return asynchronously
                this(Object.keys(store));
            }
        },
        delete: {
            success: function() {
                alert('Donor deleted.');

                clearDonorForm();
            }
        }
    };

    function getDonorInfo(event, ui) {
        // uniqueName = donor_name + (optional)id
        var uniqueName = (ui && ui.item && ui.item.value) || event.target.value;

        if (!uniqueName || uniqueName === "") {
            clearDonorForm();
            return;
        }
        // QUESTION: What is this util.check checking for?
        if (util.check("name", uniqueName)) {
            return;
        }

        setDonorForm(store[uniqueName]);
    }

    /**
     * Takes a Donor and sets form data accordingly
     * @param {Donor} data
     */
    function setDonorForm(data = {}) {
        if (!data) {
            clearDonorForm();
            return;
        }

        donor = new Donor(data);

        dom.input.donorName.value = data.donor_name;
        dom.input.id.value = data.id;
        dom.input.email.value = data.email;
        dom.input.telephoneNumber.value = data.telephone_number;
        dom.input.mobileNumber.value = data.mobile_number;
        dom.input.customerRef.value = data.customer_ref;
        dom.input.wantReceipt.value = data.want_receipt;
        dom.input.addressLine.value = data.address_line;
        dom.input.city.value = data.city;
        dom.input.province.value = data.province;
        dom.input.postalCode.value = data.postal_code;

        util.setButton(dom.button, "existing");

        donation.getDonation(data.id);
    }

    /**
     * Resets all Donor related input and clearDonation
     */
    function clearDonorForm() {
        util.emptyAllFields(dom.input);
        util.setButton(dom.button, "new");

        donation.getDonation(null);
    }


    /**
     * REQUIRE: this.donor.input.name == name field
     * EFFECT: calls for a list of names
     */
    function getNames(request, response) {
        Donor.autocomplete(request.term, callback.get.success.bind(response));
        // util.ajax({
        //     type: "GET",
        //     url: "/api/autocomplete_name",
        //     data: { key: dom.input.name.value },
        //     // QUESTION: Is this the only way? Couldn't we just use promises?
        //     success: callback.get.success.bind(response),
        //     error: callback.get.fail
        // });
    }

    /**
     *
     */
    function updateDonor() {
        var data = $(dom.form).serializeArray();
        // Removes comma and ID from donor name field
        var uniqueName = data[1].value;
        data[1].value = uniqueName.split(', ')[0];
        var jsonObject = {};
        // Trasform data array into a JSON Object
        for (var i = 0; i < data.length; i++) {
            jsonObject[data[i].name] = data[i].value;
        }
        // Insert id from uniqueName
        jsonObject.id = uniqueName.split(', ')[1];

        donor = new Donor(jsonObject);

        donor.update(callback.put.success);
        // util.ajax({
        //     url: "/api/donor",
        //     type: "PUT",
        //     data: data,
        //     success: callback.put.success,
        //     error: callback.put.fail
        // });
    }

    /**
     * delete donor using id
     */
    function deleteDonor() {
        donor.delete(callback.delete.success);
        // util.ajax({
        //     url: "/api/donor",
        //     type: "DELETE",
        //     data: { donor_id: dom.input.id.value },
        //     success: callback.delete.success,
        //     error: callback.delete.fail
        // });
    }

    /**
     * when saved need
     */
    function saveNewDonor() {
        var data = $(dom.form).serialize();
        // No need to split id as new entries do not have an id
        donor = new Donor(data);
        donor.save(callback.post.success);
        // util.ajax({
        //     url: "/api/donor",
        //     type: "POST",
        //     data: $(dom.form).serialize(),
        //     success: callback.post.success,
        //     error: callback.post.fail
        // });
    }

    /**
     * request list of names for autocomplete
     *
     * minLength : minimum length required to execute ajax
     * { key : <string> }
     *  response data = [ <name1>, <name2>]
     */
    $(dom.input.donorName).autocomplete({
        source: getNames,
        minLength: 2,
        select: getDonorInfo
    });
    $(dom.input.donorName).on("blur", getDonorInfo);
    $(dom.button.save).on("click", saveNewDonor);
    $(dom.button.delete).on("click", deleteDonor);
    $(dom.button.update).on("click", updateDonor);

    return {};
});
