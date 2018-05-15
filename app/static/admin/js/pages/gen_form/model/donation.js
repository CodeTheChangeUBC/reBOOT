define(["../util/util", "./item", "../view/donation"], function (util, item, dom) {

    var callback = {
        get: {
            success: function () {
                printDonationList.apply(this, arguments);
            },
            fail: function () {
                console.error(arguments);
            }
        },
        put: {
            success: function (response) {
                alert('Donation updated. [tax receipt no: ' + response.tax_receipt_no + ']');
                getDonation(dom.input.donorId.value, response.tax_receipt_no);
            },
            fail: function () {
                console.error(arguments);
            }
        },
        post: {
            success: function (response) {
                alert('New donation saved. [tax receipt no: ' + response.tax_receipt_no + ']');
                getDonation(dom.input.donorId.value);
            },
            fail: function () {
                console.error(arguments);
            }
        },
        delete: {
            success: function () {
                console.log('Deleted');
                getDonation(dom.input.donorId.value);
            },
            fail: function () {
                console.error(arguments);
            }
        }
    };

    var store = {};
    var getDonation = function (donor_id, tax_receipt_no) {
        if (donor_id == null) {
            printDonationList([]);
            return;
        }

        store = {};
        store.donor_id = donor_id;

        util.ajax({
            type: "GET",
            url: "/api/donation",
            data: { donor_id: donor_id },
            success: callback.get.success,
            error: callback.get.fail
        });
    };

    var setDonationForm = function (e, data) {
        // [1] donor name not present
        if (this == dom.button.addNew && !util.isDonorNamePresent()) {
            util.enterDonorName();
            return;
        }

        // [2] create new donation
        if (this == dom.button.addNew) {
            util.emptyAllFields(dom.input);             // empty donation input fields
            item.clearItemView();                       // clear items table and form
            util.setButton(dom.button, "new");          // show appropriate button for new data
            dom.div.form.hidden         = false;        // make sure form is shown
            dom.div.taxReceiptNo.hidden = true;         // tax_receipt_no field is hidden
            util.scrollTo(dom.input.date);              // scroll to input date
            // QUESTION: What's the purpose of using store value?
            dom.input.donorId.value = store.donor_id;   // set donor id into a form field
            return;
        }

        // [3] event when form needs to be closed
        if (this == dom.button.cancel || !data) {
            dom.div.form.hidden     = true;             // hide form
            // dom.div.header.hidden   = true;          // header no longer used

            util.emptyAllFields(dom.input);             // clear out the input fields
            item.clearItemView();                       // clear items table
            util.setButton(dom.button, null);           // set button to a default
            return;
        }

        // set form iff data.tax_receipt_no match with the last selected donation.
        if (!util.check('tax_receipt_no', data.tax_receipt_no)) return;

        // [4] event to set form with data
        util.setButton(dom.button, "existing");

        // set input fields with data
        dom.input.donorId.value             = data.donor_id_id;
        dom.input.taxReceiptNo.value        = data.tax_receipt_no || "";
        dom.input.date.value                = data.donate_date || "";
        dom.input.isVerified.checked        = data.verified;
        dom.input.pickUpPostalCode.value    = data.pick_up || "";

        // show form fields
        dom.div.taxReceiptNo.hidden = false;
        dom.div.form.hidden         = false;
    };

    var clearDonationForm = function() {
        // QUESTION: What's the point of calling [3] if it can just be done here?
        setDonationForm.call(this, null); // calls [3]
    };

    var printDonationList = function (data) {

        var html = "";
        var donation;

        for (var ix = 0; data && ix < data.length; ix++) {
            donation = data[ix];
            store[donation.tax_receipt_no] = donation;
            html +=
                '<tr class="row' +
                (ix % 2 ? 2 : 1) +
                '" id="' +
                donation.tax_receipt_no +
                '" >\n' +
                '    <td class="field-tax_receipt_no">' +
                donation.tax_receipt_no +
                "</td>\n" +
                '    <td class="field-donate_date nowrap">' +
                donation.donate_date +
                "</td>\n" +
                '    <td class="field-pick_up">' +
                donation.pick_up +
                "</td>\n" +
                '    <td class="field-verified">' +
                (donation.verified
                    ? '<img src="/static/admin/img/icon-yes.svg" alt=true>'
                    : '<img src="/static/admin/img/icon-no.svg" alt=false>') +
                "    </td>\n" +
                "</tr>";
        }

        clearDonationForm();
        dom.table.tbody.innerHTML = html;
    };

        var saveDonation = function () {
            if (!store.donor_id) alert("Save donor first");
            util.ajax({
                url: "/api/donation",
                type: "POST",
                data: $(dom.form).serialize(),
                success: callback.post.success,
                error: callback.post.fail
            });
        };

        var updateDonation = function() {
            util.ajax({
                url: "/api/donation",
                type: "PUT",
                data: $(dom.form).serialize(),
                success: callback.put.success,
                error: callback.put.fail
            });
        };

        var deleteDonation = function() {
            util.ajax({
                url: "/api/donation",
                type: "DELETE",
                data: { tax_receipt_no: dom.input.taxReceiptNo.value },
                success: callback.delete.success,
                error: callback.delete.fail
            });
        };

        function isSameAsCurrent(tax_receipt_no) {
            return util.check('tax_receipt_no', tax_receipt_no);
        }

        $(dom.table.tbody).on("click", "tr", function (e) {
            var tr = this.children;

            var tax_receipt_no = tr[0].innerText;
            var data = {};

            if (isSameAsCurrent(tax_receipt_no)) return;

            setDonationForm(e, store[tax_receipt_no]);
            item.getItems.call(this, tax_receipt_no);
            util.scrollTo(this);
        });
        $(dom.button.addNew).on("click", setDonationForm);
        $(dom.button.cancel).on("click", setDonationForm);
        $(dom.button.delete).on("click", deleteDonation);
        $(dom.button.save).on("click", saveDonation);
        $(dom.button.update).on("click", updateDonation);

        return {
            // QUESTION: Delete unused functions
            printDonationList: printDonationList,
            getDonation: getDonation
        };
    }.bind({})
);
