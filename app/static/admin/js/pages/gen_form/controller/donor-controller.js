"use strict";
define(["../util/util", "../model/donation", "../view/donor-view", "../model/donor"], function(util, donation, dom, Donor) {

    // An instance of donor used frequently for data
    var donor = new Donor();
    // Donors used to keep track of result from autocomplete
    var donors = {};


    var callback = {
        post: {
            success: function(donorData) {
                donor = new Donor(donorData);
                alert(donor.donor_name + ' saved.');
                var uniqueName = donor.uniqueName();
                donors[uniqueName] = donor;
                dom.input.name.value = uniqueName;
                setDonorForm(donors[uniqueName]);
            }
        },
        put: {
            success: function(donor) {
                alert(donor.donor_name + ' updated.');
                var uniqueName = donor.uniqueName();
                donors[uniqueName] = donor;
                dom.input.name.value = uniqueName;
            }
        },
        get: {
            success: function(data) {
                donors = {};
                data.reduce(function(donors, donorData) {
                    var donor = new Donor(donorData);
                    donors[donor.uniqueName()] = donor;
                    return donors;
                }, donors);

                // Requires binding to response from autocomplete in order to return asynchronously
                this(Object.keys(donors));
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

        if (isNewDonor(uniqueName)) {
            clearDonorFormExceptName();
            return;
        }

        setDonorForm(donors[uniqueName]);
    }

    function isNewDonor(donorName) {
        return donorName.split(', ').length < 2;
    }

    /**
     * Takes a Donor and sets form data accordingly
     * @param {Donor} data
     */
    function setDonorForm(data = {}) {
        if (!data || $.isEmptyObject(data)) {
            clearDonorFormExceptName();
            return;
        }

        donor = data;

        dom.input.id.value = data.id;
        dom.input.donorName.value = data.donor_name;
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
     * Resets all Donor related input and clearDonation
     */
    function clearDonorFormExceptName() {
        util.emptyAllFields(dom.input, [dom.input.donorName]);
        util.setButton(dom.button, "new");

        donation.getDonation(null);
    }

    /**
     * EFFECT: calls for a list of names
     */
    function getNames(request, response) {
        Donor.autocomplete(request.term, callback.get.success.bind(response));
    }

    /**
     *
     */
    function updateDonor() {
        var data = $(dom.form).serializeArray();
        // Trasform data array into a JSON Object
        var jsonObject = {};
        for (var i = 0; i < data.length; i++) {
            jsonObject[data[i].name] = data[i].value;
        }
        donor = new Donor(jsonObject);

        donor.update(callback.put.success);
    }

    /**
     * delete donor using id
     */
    function deleteDonor() {
        donor.delete(callback.delete.success);
    }

    /**
     * when saved need
     */
    function saveNewDonor() {
        var data = $(dom.form).serialize();
        donor = new Donor(data);
        donor.save(callback.post.success);
    }

    /**
     * DOM event bindings
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
