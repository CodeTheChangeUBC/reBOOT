define(["./form-util", "./form-donation"], function (util, donation) {
    /**
     * Donor form fields
     */
    var dom = {
        button: {
            delete  : document.getElementById("btn_delete_donor"),
            save    : document.getElementById("btn_save_donor"),
            update  : document.getElementById("btn_update_donor")
        },
        input: {
            id      : document.getElementById("id_donor_id"),
            name    : document.getElementById("id_donor_name"),
            email   : document.getElementById("id_email"),
            telephone: document.getElementById("id_telephone_number"),
            mobile  : document.getElementById("id_mobile_number"),
            ref     : document.getElementById("id_customer_ref"),
            needReceipt: document.getElementById("id_want_receipt"),
            address : document.getElementById("id_address_line"),
            city    : document.getElementById("id_city"),
            province: document.getElementById("id_province"),
            postalCode: document.getElementById("id_postal_code")
        },
        form: document.getElementById("donor_form")
    };

    var callback = {
        post: {
            success: function (donor) {
                alert(donor.donor_name + ' saved.');
                store = {};
                var str = donor.donor_name + ', ' + donor.id;
                store[str] = donor;
                dom.input.name.value(str);
            },
            fail: function () {
                console.error(arguments); // debug
            }
        },
        put: {
            success: function (donor) {
                alert(donor.donor_name + ' updated.');
                store = {};
                var str = donor.donor_name + ', ' + donor.id;
                store[str] = donor;
                dom.input.name.value(str);
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
            },
            fail: function () {
                console.error(arguments);
            }
        },
        delete: {
            success: function (donor) {
                alert('Deleted.');
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
            setDonorForm.apply(null, null);
            return;
        }

        if (util.check("name", nameId)) return;

        setDonorForm(store[nameId]);
    }.bind(this);

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

    var store = {};

    /**
     * REQUIRE: this.donor.input.name == name field
     * EFFECT: calls for a list of names
     */
    function getNames(request, response) {
        $.ajax({
            url: "/api/autocomplete_name",
            dataType: "json",
            data: { key: dom.input.name.value },
            success: response.get.success,
            error: response.get.fail
        });
    }

    /**
     *
     */
    function updateDonor() {
        var data = JSON.parse($(dom.form).serialize());
        data['donor_name'] =data['donor_name'].split(',')[0];

        $.ajax({
            beforeSend: util.csrf,
            url: "/api/donor",
            type: "PUT",
            dataType: "json",
            data: data.toString(),
            success: callback.put.success,
            error: callback.put.fail
        });
    }

    /**
     * delete donor using id
     */
    function deleteDonor() {
        $.ajax({
            beforeSend: util.csrf,
            url: "/api/donor",
            type: "DELETE",
            dataType: "json",
            data: { donor_id: dom.input.id.value },
            success: callback.delete.success,
            error: callback.delete.fail
        });
    }

    /**
     * when saved need
     */
    function saveNewDonor() {
        $.ajax({
            beforeSend: util.csrf,
            url: "/api/donor",
            type: "POST",
            dataType: "json",
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
