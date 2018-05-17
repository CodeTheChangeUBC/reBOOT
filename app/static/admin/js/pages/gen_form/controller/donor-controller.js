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
                var uniqueName = donor.uniqueName();
                donors[uniqueName] = donor;
                alert(donor.donorName + ' saved.');
                setDonorForm(donors[uniqueName]);
            }
        },
        put: {
            success: function(donorData) {
                donor = new Donor(donorData);
                var uniqueName = donor.uniqueName();
                donors[uniqueName] = donor;
                alert(donor.donorName + ' updated.');
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
        // uniqueName = donorName + (optional)id
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
        dom.input.donorName.value = data.donorName;
        dom.input.email.value = data.email;
        dom.input.telephoneNumber.value = data.telephoneNumber;
        dom.input.mobileNumber.value = data.mobileNumber;
        dom.input.customerRef.value = data.customerRef;
        dom.input.wantReceipt.value = data.wantReceipt;
        dom.input.addressLine.value = data.addressLine;
        dom.input.city.value = data.city;
        dom.input.province.value = data.province;
        dom.input.postalCode.value = data.postalCode;

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
        donor = new Donor(util.serializeObject(dom.form));
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
        donor = new Donor(util.serializeObject(dom.form));
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
