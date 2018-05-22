"use strict";
define(["../util/util", "../model/donation", "../controller/item-controller", "../view/donation"], function(util, Donation, itemCtrl, dom) {

    var currentDonorId;
    var currentDonation = new Donation();
    var donations = {};

    var callback = {
        related: {
            success: function(response) {
                donations = {};
                for (var i = 0; response && i < response.length; i++) {
                    var donation = response[i];
                    donation.donorId = currentDonorId;
                    donations[donation.taxReceiptNo] = new Donation(donation);
                }
                printDonationList(donations);
            }
        },
        get: {
            success: function( /* reponse */ ) {
                // new Donation(response);
            }
        },
        post: {
            success: function(response) {
                currentDonation = new Donation(response);
                donations[currentDonation.taxReceiptNo] = currentDonation;
                alert('New donation [Tax receipt no: ' + currentDonation.taxReceiptNo + '] saved.');
                printDonationList(donations);
            }
        },
        put: {
            success: function(response) {
                currentDonation = new Donation(response);
                donations[currentDonation.taxReceiptNo] = currentDonation;
                alert('Donation updated. [Tax receipt no: ' + currentDonation.taxReceiptNo + ']');
                printDonationList(donations);
            }
        },
        delete: {
            success: function() {
                var tempTaxReceiptNo = currentDonation.taxReceiptNo;
                delete donations[tempTaxReceiptNo];
                printDonationList(donations);
                alert('Donation [Tax receipt no: ' + tempTaxReceiptNo + '] deleted');
            }
        }
    };

    var saveDonation = function() {
        if (!currentDonorId) {
            alert("Save donor first");
        }
        currentDonation = new Donation(util.serializeObject(dom.form));
        currentDonation.save(callback.post.success);
    };

    var updateDonation = function() {
        currentDonation = new Donation(util.serializeObject(dom.form));
        currentDonation.update(callback.put.success);
    };

    var deleteDonation = function() {
        currentDonation = new Donation(util.serializeObject(dom.form));
        currentDonation.delete(callback.delete.success);
    };

    var getDonation = function(donorId) {
        if (!donorId) {
            printDonationList();
            return;
        }

        dom.input.donorId.value = donorId;
        currentDonorId = donorId;

        Donation.getRelated(donorId, callback.related.success);
    };

    var setDonationForm = function(data = {}) {
        if (!data || $.isEmptyObject(data)) {
            clearDonationForm();
            return;
        }

        currentDonation = data;
        currentDonorId = data.donorId;
        // set input fields with data
        dom.input.donorId.value = data.donorId;
        dom.input.taxReceiptNo.value = data.taxReceiptNo || "";
        dom.input.date.value = data.donateDate || "";
        dom.input.isVerified.checked = data.verified;
        dom.input.pickUpPostalCode.value = data.pickUp || "";

        // show form fields
        dom.div.taxReceiptNo.hidden = false;
        dom.div.form.hidden = false;

        util.setButton(dom.button, "existing");
    };

    function addNewDonationAction() {
        if (!util.isDonorNamePresent()) {
            util.enterDonorName();
            return;
        }

        util.emptyAllFields(dom.input, [dom.input.donorId]); // empty donation input fields
        itemCtrl.clearItemView(); // clear items table and form
        util.setButton(dom.button, "new"); // show appropriate button for new data
        dom.div.form.hidden = false; // make sure form is shown
        dom.div.taxReceiptNo.hidden = true; // taxReceiptNo field is hidden
        util.scrollTo(dom.input.date); // scroll to input date
    }

    function clearDonationFormExceptDonorId() {
        dom.div.form.hidden = true; // hide form
        util.emptyAllFields(dom.input, [dom.input.donorId]); // clear out the input fields
        itemCtrl.clearItemView(); // clear items table
        util.setButton(dom.button, null); // set button to a default
    }

    function clearDonationForm() {
        dom.div.form.hidden = true; // hide form
        util.emptyAllFields(dom.input); // clear out the input fields
        itemCtrl.clearItemView(); // clear items table
        util.setButton(dom.button, null); // set button to a default
    }

    function printDonationList(data = {}) {

        var html = "";
        var count = 0;

        $.each(data, function(key, donation) {
            html += formatHtml(donation, count);
            count++;
        });

        if (currentDonorId !== parseInt(dom.input.donorId.value)) {
            clearDonationForm();
        } else {
            clearDonationFormExceptDonorId();
        }

        dom.table.tbody.innerHTML = html;
    }

    function formatHtml(donation, count) {
        var rowId = (count % 2 ? 2 : 1);
        return '<tr class="row' + rowId + '">\n' +
            '<td class="field-tax_receipt_no">' + donation.taxReceiptNo + '</td>' +
            '<td class="field-donate_date nowrap">' + donation.donateDate + '</td>\n' +
            '<td class="field-pick_up">' + donation.pickUp + '</td>\n' +
            '<td class="field-verified">' +
            (donation.verified ?
                '<img src="/static/admin/img/icon-yes.svg" alt=true>' :
                '<img src="/static/admin/img/icon-no.svg" alt=false>') +
            '</td>\n' +
            '</tr>';
    }

    function isSameAsCurrent(taxReceiptNo) {
        return currentDonation.taxReceiptNo === taxReceiptNo;
    }

    $(dom.table.tbody).on("click", "tr", function() {
        var tr = this.children;
        var taxReceiptNo = tr[0].innerText;

        if (isSameAsCurrent(taxReceiptNo)) {
            clearDonationForm();
        }

        setDonationForm(donations[taxReceiptNo]);
        itemCtrl.getItems(taxReceiptNo);
        util.scrollTo(this);
    });
    $(dom.button.addNew).on("click", addNewDonationAction);
    $(dom.button.cancel).on("click", clearDonationForm);
    $(dom.button.delete).on("click", deleteDonation);
    $(dom.button.save).on("click", saveDonation);
    $(dom.button.update).on("click", updateDonation);

    return {
        getDonation: getDonation
    };
});
