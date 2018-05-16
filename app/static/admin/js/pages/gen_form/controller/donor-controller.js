"use strict";
define(["../util/util", "../model/donation", "../view/donor-view", "../model/donor"], function(util, donation, dom, Donor) {

    // An instance of donor used frequently for data
    var donor = new Donor();
    // Donors used to keep track of result from autocomplete
    // Needed for when user selects option from autocomplete
    var donors = {};


    // Callbacks for related API calls
    var callback = {
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
        delete: {
            success: function() {
                alert('Donor deleted.');
                clearDonorForm();
            }
        }
    };


    /**
     * Get related donor information
     * Use either the user select from autocomplete or ui
     * Clear form partially/completely if donor is new.
     * @param {Event} event
     * @param {DOMElement} ui
     */
    function getDonorInfo(event, ui) {
        // uniqueName = donor_name + (optional)id
        // ie) 'test, 1' or 'test'
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

    /**
     * Helper function for checking if donor is new
     * @param {String} donorName
     */
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
        // Update the current donor
        donor = data;
        // Update the DOM fields to match the current donor
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
        // Get related donations
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
     * Resets all Donor related input and clearDonation except donor name field
     */
    function clearDonorFormExceptName() {
        util.emptyAllFields(dom.input, [dom.input.donorName]);
        util.setButton(dom.button, "new");

        donation.getDonation(null);
    }

    /**
     * Call for related donor information and bind to autocomplete response
     * This function must asynchronously bind and return to response.
     */
    function getNames(request, response) {
        Donor.autocomplete(request.term, callback.get.success.bind(response));
    }

    /**
     * Serialize the existing form and update with new data
     */
    function updateDonor() {
        var data = $(dom.form).serializeArray();
        // Trasform data array into an object
        var tempObj = {};
        for (var i = 0; i < data.length; i++) {
            tempObj[data[i].name] = data[i].value;
        }
        donor = new Donor(tempObj);
        donors[donor.uniqueName()] = donor;

        donor.update(callback.put.success);
    }

    /**
     * Delete current donor
     */
    function deleteDonor() {
        donor.delete(callback.delete.success);
    }

    /**
     * Save current donor assuming they are new
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
