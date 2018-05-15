define(["../util/util", "./donation", "../view/donor"], function (util, donation, dom) {


    var callback = {
        post: {
            success: function (donor) {
                alert(donor.donor_name + ' saved.');
                store = {};
                // QUESTION: camelCase these.
                var str = donor.donor_name + ', ' + donor.id;
                store[str] = donor;
                dom.input.name.value = str;
                setDonorForm(store[str]);
            },
            fail: function () {
                // QUESTION: Remove any debugging statement and return useful message for the user.
                console.error(arguments); // debug
            }
        },
        put: {
            success: function (donor) {
                alert(donor.donor_name + ' updated.');
                store = {};
                var str = donor.donor_name + ', ' + donor.id;
                store[str] = donor;
                dom.input.name.value = str;
            },
            fail: function () {
                console.error(arguments);
            }
        },
        get: {
            success: function (data) {
                store = {};
                data.reduce(function (store, donor) {
                    var str = donor.donor_name + ', ' + donor.id;
                    store[str] = donor;
                    return store;
                }, store);

                // QUESTION: What's the point of using this() in here? Couldn't we just return Object.keys(store)?
                // May be related to binding to response autocomplete
                this(Object.keys(store));
            },
            fail: function () {
                console.error(arguments);
            }
        },
        delete: {
            success: function (donor) {
                alert('Deleted.');
                // QUESTION: It probably is easier to understand if the setDonorForm rather took an empty object than null.
                setDonorForm(null);
            },
            fail: function() {
                alert("failed");
            }
        }
    };

    var getDonorInfo = function (e, ui) {
        var nameId = (ui && ui.item && ui.item.value) || e.target.value;

        if (!nameId || nameId == "") {
            // QUESTION: What does apply do?
            setDonorForm.apply(null, null);
            return;
        }
        // QUESTION: What is this util.check checking for?
        if (util.check("name", nameId)) return;

        setDonorForm(store[nameId]);
    }.bind(this);
    // QUESTION: Used to keep the scope of original caller

    var setDonorForm = function (data) {
        if (!data) {
            util.emptyAllFields(this.input, [this.input.name]);
            util.setButton(this.button, "new");

            donation.getDonation(null);
            return;
        }

        this.input.name.value       = data.donor_name;
        this.input.id.value         = data.id;
        this.input.email.value      = data.email;
        this.input.telephone.value  = data.telephone_number;
        this.input.mobile.value     = data.mobile_number;
        this.input.ref.value        = data.customer_ref;
        this.input.needReceipt.value = data.want_receipt;
        this.input.address.value    = data.address_line;
        this.input.city.value       = data.city;
        this.input.province.value   = data.province;
        this.input.postalCode.value = data.postal_code;

        util.setButton(this.button, "existing");

        donation.getDonation(data.id);
    }.bind(dom);
    // QUESTION: What is the purpose behind doing bind on here?

    // QUESTION: What is this store for? Is it for caching variables? Seems to be some sort of storage for API call store.
    var store = {};

    /**
     * REQUIRE: this.donor.input.name == name field
     * EFFECT: calls for a list of names
     */
    function getNames(request, response) {
        util.ajax({
            type: "GET",
            url: "/api/autocomplete_name",
            data: { key: dom.input.name.value },
            // QUESTION: Is this the only way? Couldn't we just use promises?
            success: callback.get.success.bind(response),
            error: callback.get.fail
        });
    }

    /**
     *
     */
    function updateDonor() {
        var data = $(dom.form).serializeArray();
        // QUESTION: Remove comma and ID from donor name field
        data[1].value = data[1].value.split(',')[0];

        util.ajax({
            url: "/api/donor",
            type: "PUT",
            data: data,
            success: callback.put.success,
            error: callback.put.fail
        });
    }

    /**
     * delete donor using id
     */
    function deleteDonor() {
        util.ajax({
            url: "/api/donor",
            type: "DELETE",
            data: { donor_id: dom.input.id.value },
            success: callback.delete.success,
            error: callback.delete.fail
        });
    }

    /**
     * when saved need
     */
    function saveNewDonor() {
        util.ajax({
            url: "/api/donor",
            type: "POST",
            data: $(dom.form).serialize(),
            success: callback.post.success,
            error: callback.post.fail
        });
    }

    /**
     * request list of names for autocomplete
     *
     * minLength : minimum length required to execute ajax
     * { key : <string> }
     *  response data = [ <name1>, <name2>]
     */
    $(dom.input.name).autocomplete({
        source: getNames.bind(this),
        minLength: 2,
        select: getDonorInfo
    });
    $(dom.input.name).on("blur", getDonorInfo);
    $(dom.button.save).on("click", saveNewDonor);
    $(dom.button.delete).on("click", deleteDonor);
    $(dom.button.update).on("click", updateDonor);

    return {};
}.bind({}));
