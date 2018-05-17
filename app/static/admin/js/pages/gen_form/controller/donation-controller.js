"use strict";
define(["../util/util", "../model/donation", "../model/item", "../view/donation"], function(util, Donation, item, dom) {

    var currentDonorId;
    var currentDonation = new Donation();
    var donations = {};

    var callback = {
        related: {
            success: function(response) {
                donations = {};
                for (var i = 0; response && i < response.length; i++) {
                    var donation = response[i];
                    donation.donor_id = currentDonorId;
                    donations[donation.tax_receipt_no] = new Donation(donation);
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
                donations[currentDonation.tax_receipt_no] = currentDonation;
                alert('New donation [Tax receipt no: ' + currentDonation.tax_receipt_no + '] saved.');
                printDonationList(donations);
            }
        },
        put: {
            success: function(response) {
                currentDonation = new Donation(response);
                donations[currentDonation.tax_receipt_no] = currentDonation;
                alert('Donation updated. [tax receipt no: ' + currentDonation.tax_receipt_no + ']');
                printDonationList(donations);
            }
        },
        delete: {
            success: function() {
                var tempTaxReceiptNo = currentDonation.tax_receipt_no;
                delete donations[currentDonation.tax_receipt_no];
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

    var getDonation = function(donor_id) {
        if (!donor_id) {
            printDonationList();
            return;
        }

        dom.input.donorId.value = donor_id;
        currentDonorId = donor_id;

        Donation.getRelated(donor_id, callback.related.success);
    };

    var setDonationForm = function(data = {}) {
        if (!data || $.isEmptyObject(data)) {
            clearDonationForm();
            return;
        }

        currentDonation = data;
        currentDonorId = data.donor_id;
        // set input fields with data
        dom.input.donorId.value = data.donor_id;
        dom.input.taxReceiptNo.value = data.tax_receipt_no || "";
        dom.input.date.value = data.donate_date || "";
        dom.input.isVerified.checked = data.verified;
        dom.input.pickUpPostalCode.value = data.pick_up || "";

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
        item.clearItemView(); // clear items table and form
        util.setButton(dom.button, "new"); // show appropriate button for new data
        dom.div.form.hidden = false; // make sure form is shown
        dom.div.taxReceiptNo.hidden = true; // tax_receipt_no field is hidden
        util.scrollTo(dom.input.date); // scroll to input date
    }

    function clearDonationFormExceptDonorId() {
        dom.div.form.hidden = true; // hide form
        util.emptyAllFields(dom.input, [dom.input.donorId]); // clear out the input fields
        item.clearItemView(); // clear items table
        util.setButton(dom.button, null); // set button to a default
    }

    function clearDonationForm() {
        dom.div.form.hidden = true; // hide form
        util.emptyAllFields(dom.input); // clear out the input fields
        item.clearItemView(); // clear items table
        util.setButton(dom.button, null); // set button to a default
    }

    function printDonationList(data = {}) {

        var html = "";
        var count = 0;

        $.each(data, function(key, donation) {
            html += formatHtml(donation, count);
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
            '<td class="field-tax_receipt_no">' + donation.tax_receipt_no + '</td>' +
            '<td class="field-donate_date nowrap">' + donation.donate_date + '</td>\n' +
            '<td class="field-pick_up">' + donation.pick_up + '</td>\n' +
            '<td class="field-verified">' +
            (donation.verified ?
                '<img src="/static/admin/img/icon-yes.svg" alt=true>' :
                '<img src="/static/admin/img/icon-no.svg" alt=false>') +
            '</td>\n' +
            '</tr>';
    }

    function isSameAsCurrent(tax_receipt_no) {
        return currentDonation.tax_receipt_no === tax_receipt_no;
    }

    $(dom.table.tbody).on("click", "tr", function() {
        var tr = this.children;
        var tax_receipt_no = tr[0].innerText;

        if (isSameAsCurrent(tax_receipt_no)) {
            clearDonationForm();
        }

        setDonationForm(donations[tax_receipt_no]);
        // TODO: Fix this
        item.getItems.call({
            id: tax_receipt_no
        });
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
