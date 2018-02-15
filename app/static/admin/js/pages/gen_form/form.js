/**
 * TODO
 * [1] recognizing when new donor entered
 * - when name input field unfocused,
 */

var Form = function () {
    var _this = this;

    /**
     * Donor form fields
     */
    this.donor = {
        button: {
            delete              : document.getElementById("btn_delete_donor"),
            save                : document.getElementById("btn_save_donor"),
            update              : document.getElementById("btn_update_donor")
        },
        input: {
              name              : document.getElementById("id_donor_name"),
              email             : document.getElementById("id_email"),
              telephone         : document.getElementById("id_telephone_number"),
              mobile            : document.getElementById("id_mobile_number"),
              ref               : document.getElementById("id_customer_ref"),
              needReceipt       : document.getElementById("id_want_receipt"),
              address           : document.getElementById("id_address_line"),
              city              : document.getElementById("id_city"),
              province          : document.getElementById("id_province"),
              postalCode        : document.getElementById("id_postal_code")
        }
    };

    /**
     * Donation table & form fields
     */
    this.donation = {
        div: {
            header              : document.getElementById("donation_header"),
            form                : document.getElementById("donation_form"),
            taxReceiptNo        : document.getElementById("donation_form").getElementsByClassName("field-tax_receipt_no")[0]
        },
        form                    : $(document.getElementById("donation_form").getElementsByTagName("form")[0]),
        table: {
            tbody               : document.getElementById("donation_result_list").getElementsByTagName("tbody")[0]
        },
        button: {
            delete              : document.getElementById("btn_delete_donation"),
            save                : document.getElementById("btn_save_donation"),
            update              : document.getElementById("btn_update_donation"),
            addNew              : document.getElementById("btn_add_new_donation"),
            cancel              : document.getElementById("btn_cancel_donation"),
        },
        input: {
            taxReceiptNo        : document.getElementById("id_tax_receipt_no"),
            date                : document.getElementById("id_donate_date"),
            isVerified          : document.getElementById("id_verified"),
            pickUpPostalCode    : document.getElementById("id_pick_up")
        }
    };

    /**
     * Items table & form fields
     */
    this.item = {
        div: {
            container           : document.getElementById('item_container'),
            header              : document.getElementById('item_header'),
            form                : document.getElementById('item_form')
        },
        table: {
            tbody               : document.getElementById('item_result_list').getElementsByTagName('tbody')[0]
        },
        button: {
            delete              : document.getElementById('btn_delete_item'),
            save                : document.getElementById('btn_save_item'),
            update              : document.getElementById('btn_update_item'),
            addNew              : document.getElementById('btn_add_new_item'),
            cancel              : document.getElementById('btn_cancel_item')
        },
        input: {
            taxReceiptNo        : document.getElementById('id_tax_receipt_no_for_item'),
            itemId              : document.getElementById('id_item_id'),
            description         : document.getElementById('id_description'),
            particulars         : document.getElementById('id_particulars'),
            manufacturer        : document.getElementById('id_manufacturer'),
            model               : document.getElementById('id_model'),
            quantity            : document.getElementById('id_quantity'),
            isWorking           : document.getElementById('id_working'),
            condition           : document.getElementById('id_condition'),
            quality             : document.getElementById('id_quality'),
            isVerified          : document.getElementById('id_item_verified'),
            batch               : document.getElementById('id_batch'),
            value               : document.getElementById('id_value')
        }
    };

    var set = function() {
        this._ = this._ || {};
        var _ = this._;
        return function(key, value) {
            _[key] = value;
        };
    }();

    var get = function(key) {
        return this._[key];
    }.bind(this._);

    var check = function () {
        var _ = this._;
        return function(key, value) {
            if (_[key] == undefined || _[key] != value) {
                set(key, value);
                return false;
            }
            return true;
        }
    }();

    /**
     * REQUIRE: dom variables set
     * MODIFIES: dom
     * EFFECT: change button visibilities
     * SCOPE: this.donor | this.donation | this.item
     */
    var setButton = function(button, type) {
        switch(type) {
            case 'new':
                button.delete.hidden      = true;
                button.save.hidden        = false;
                button.update.hidden      = true;
                button.addNew? button.addNew.hidden = true  : null;
                button.cancel? button.cancel.hidden = false : null;
                break;
            case 'existing':
                button.delete.hidden      = false;
                button.save.hidden        = true;
                button.update.hidden      = false;
                button.addNew? button.addNew.hidden = true  : null;
                button.cancel? button.cancel.hidden = false : null;
                break;
            default:
                button.delete.hidden      = true;
                button.save.hidden        = true;
                button.update.hidden      = true;
                button.addNew? button.addNew.hidden = false : null;
                button.cancel? button.cancel.hidden = true  : null;
        }
    };

    /**
     * REQUIRE: input = { key : dom }
     * MODIFIES: input
     * EFFECT: reset form fields to null
     */
    var emptyAllFields = function (input, exceptions) {
        var inputNames = Object.keys(input);
        var ix = inputNames.length;
        var node;

        while(ix--) {
            node = input[inputNames[ix]];

            if (exceptions && exceptions.includes && exceptions.includes(node)) {
                continue;
            }

            if (node.type == 'checkbox') {
                node.checked = false;
                continue;
            }

            node.value = "";
        }
    };

    /**
     * REQUIRE: dom variables set
     * MODIFIES: html
     * EFFECT: set form fields with data
     */
    var setDonorForm = function (data) {

        if (!data) {
            emptyAllFields(this.input, [this.input.name]);
            setButton(this.button, 'new');
            printDonationList([]);
            return;
        }

        this.input.email.value       = data.email;
        this.input.telephone.value   = data.telephone_number;
        this.input.mobile.value      = data.mobile_number;
        this.input.ref.value         = data.customer_ref;
        this.input.needReceipt.value = data.want_receipt;
        this.input.address.value     = data.address_line;
        this.input.city.value        = data.city;
        this.input.province.value    = data.province;
        this.input.postalCode.value  = data.postal_code;

        setButton(this.button, 'existing');
        printDonationList(data.donation_records);
    }.bind(this.donor);

    /**
     * MODIFIES: this.donation
     * EFFECT: set item form fields
     * TODO event listener
     */
    var setDonationForm = function() {

        var _this           = this.donation;
        var donorName       = this.donor.input.name;

        return function (e, data) {

            // [*]
            if (this == _this.button.addNew && donorName.value == '') {
                alert("Enter donor info first");
                scrollTo(donorName);
                return;
            }

            // [2] event to open an empty form
            if (this == _this.button.addNew) {
                // _this.div.header.hidden = false;
                // _this.div.header.innerText = "New Donation";

                // TODO set donor id to the form

                emptyAllFields(_this.input);
                printItemList(null);
                setButton(_this.button, 'new');
                _this.div.form.hidden = false;

                _this.div.taxReceiptNo.hidden   = true;
                scrollTo(_this.input.date);
                return;
            }

            // [1] event when form needs to be closed
            if (this == _this.button.cancel || !data) {
                _this.div.form.hidden = true;
                _this.div.header.hidden = true;

                emptyAllFields(_this.input);
                printItemList(null);
                setButton(_this.button, null);
                return;
            }

            // [3] event to set form with data
            else {
                setButton(_this.button, 'existing');

                _this.div.taxReceiptNo.hidden = false;
                // _this.div.header.hidden = false;
                // _this.div.header.innerText = data.tax_receipt_no;

                _this.input.taxReceiptNo.value      = data.tax_receipt_no || '';
                _this.input.date.value              = data.donate_date || '';
                _this.input.isVerified.checked      = (data.verified.toUpperCase() == 'TRUE');
                _this.input.pickUpPostalCode.value  = data.pick_up || '';
            }

            _this.div.form.hidden = false;
        };
    }.call(this);

    /**
     * MODIFIES: this.item
     * EFFECT: set item form fields
     */
    var setItemForm = function() {
        var _this           = this.item;
        var donorName       = this.donor.input.name;

        return function (data) {

            // [*]
            if (this == _this.button.addNew && donorName.value == '') {
                alert("Enter donor info first");
                scrollTo(donorName);
                return;
            }

            if (!data) {
                emptyAllFields(_this.input);
                _this.div.form.hidden = true;
                setButton(_this.button, null);

                return;
            }

            if (this == _this.button.cancel) {
                emptyAllFields(_this.input);
                _this.div.form.hidden = true;
                setButton(_this.button, null);

                return;
            }

            if (this == _this.button.addNew) {
                emptyAllFields(_this.input);
                _this.div.form.hidden = false;
                setButton(_this.button, 'new');
                scrollTo(_this.input.description);

                return;
            }

            if (this == _this.button.cancel) {
                emptyAllFields(_this.input);
                _this.div.form.hidden = true;
                setButton(_this.button, null);

                return;
            }

             // TODO item id
            _this.input.taxReceiptNo.value    = data.taxReceiptNo;
            _this.input.itemId.value          = data.itemId;
            _this.input.description.value     = data.description;
            _this.input.particulars.value     = data.particulars;
            _this.input.manufacturer.value    = data.manufacturer;
            _this.input.model.value           = data.model;
            _this.input.quantity.value        = data.quantity;
            _this.input.isWorking.checked     = data.isWorking;
            _this.input.condition.value       = data.condition;
            _this.input.quality.value         = data.quality;
            _this.input.isVerified.checked    = data.isVerified;
            _this.input.batch.value           = data.batch;
            _this.input.value.value           = data.value;

            _this.div.form.hidden = false;
            setButton(_this.button, 'existing');
        }
    }.call(this);

    /**
     * print donation list
     * data = [ { tax_receipt_no : <tax_receipt_no>,
     *            donate_date : <donation_date>,
     *            pick_up : <pick_up location>
     *          }, ... ]
     */
    var printDonationList = function () {

        var donation_result_div = document.getElementById('donation_result_list');
        var donation_table_body = donation_result_div.getElementsByTagName("tbody")[0];

        return function (data) {
            var html = '';
            var donation;
            for (var ix = 0, ixLen = data.length; ix < ixLen; ix++) {
                donation = data[ix];
                html += '<tr class="row' + ((ix % 2) ? 2 : 1) + '" id="' + donation.tax_receipt_no + '" >\n' +
                    '    <td class="field-tax_receipt_no">' + donation.tax_receipt_no + '</td>\n' +
                    '    <td class="field-donate_date nowrap">' + donation.donate_date + '</td>\n' +
                    '    <td class="field-pick_up">' + donation.pick_up + '</td>\n' +
                    '    <td class="field-verified">' +
                    ((donation.verified) ? '<img src="/static/admin/img/icon-yes.svg" alt=true>' : '<img src="/static/admin/img/icon-no.svg" alt=false>') +
                    '    </td>\n' +
                    '</tr>';
            }

            setDonationForm.call(this, null);
            // scrollTo(donation_result_div);
            donation_table_body.innerHTML = html;
        };
    }();

    var printItemList = function () {
        var _this = this;

        return function (data) {

            if (!data) {
                _this.div.container.hidden = true;
                setItemForm(null);
                return;
            }

            _this.div.container.hidden = false;
            _this.div.header.value = this.id; // tax_receipt_no;

            var html = '';
            var item;
            for (var ix = 0, ixLen = data.length; ix < ixLen; ix++) {
                item = data[ix];
                html += '<tr class="row' + ((ix % 2) ? 2 : 1) + '" id="' + item.item_id + '" >\n' +
                    // '                        <td class="action-checkbox"><input type="checkbox" name="_selected_action" value='+item.item_id +'\n' +
                    // '                                                           class="action-select"></td>\n' +
                    '<td class="field-get_item">'       +item.item_id+'</td>\n' +
                    '<td class="field-manufacturer">'   +item.manufacturer+'</td>\n' +
                    '<td class="field-model">'          +item.model+'</td>\n' +
                    '<td class="field-quantity">'       +item.quantity+'</td>\n' +
                    '<td class="field-batch">'          +item.batch+'</td>\n' +
                    '<td class="field-verified">' +
                    ((item.verified) ? '<img src="/static/admin/img/icon-yes.svg" alt=true>' : '<img src="/static/admin/img/icon-no.svg" alt=false>') +
                    '</td>\n' +
                    '</tr>';
            }

            setItemForm(null);
            setButton(_this.button, null);
            // scrollTo(item_result_div);
            _this.table.tbody.innerHTML = html;
        };
    }.call(this.item);

    var csrf = function () {
        var cookie = function (name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }('csrftoken');

        return function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {// Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", cookie);
            }
        }
    }();

    var saveDonation = function () {
        $.ajax({
            beforeSend: csrf,
            url: "/add/donation",
            type: "POST",
            dataType: "json",
            data: this.serialize(),
            success: printDonationList,
            error: function () {
                console.error(arguments);
            }
        });
    }.bind(this.donation.form);

    /**
     * REQUIRE: this.donor.input.name == name field
     * EFFECT: calls for a list of names
     */
    function getNames (request, response) {
        $.ajax({
            url: "/add/autocomplete_name",
            dataType: "json",
            data: {
                key: this.donor.input.name.value
            },
            success: function (data) {
                response(data.result);
            },
            error: function () {
                console.error(arguments);
            }
        });
    }

    /**
     * request donor information & donation records
     *
     * request : { donor_name : <donor_name> }
     * response : { email : <donor_email>,
     *              telephone_numb : <telephone>,
     *              mobile_number : <mobile>,
     *              customer_ref : <customer>,
     *              want_receipt : <whether receipt requested>,
     *              address_line : <address>,
     *              city : <city>,
     *              province : <province>,
     *              postal_code : <postal_code>
     *              donation_records : [ {
     *                      tax_receipt_no : <tax_receipt_no>,
     *                      donate_date : <donation_date>,
     *                      pick_up : <pick_up location>
     *              }, ... ]
     *     }
     */
    var getDonorInfo = function (e, ui) {

        var value = ui && ui.item && ui.item.value || e.target.value;

        if (!value || value == "") {
            setDonorForm.apply(null, null);
            return;
        }

        if (check('name', value)) return;

        $.ajax({
            url: "/add/donor",
            dataType: "json",
            data: {
                donor_name: value
            },
            success: function() {
                console.log("selected result", arguments);
                setDonorForm.apply(null, arguments);
            },
            error: function () {
                console.error(arguments);
            }
        });
    }.bind(this);

    var getItems = function () {
        $.ajax({
            beforeSend: csrf,
            url: "/add/item",
            type: "GET",
            dataType: "json",
            data: {
                tax_receipt_no: this.id
            },
            success: printItemList.bind(this),
            error: function () {
                console.error(arguments);
            }
        });
    };

    var getItemInfo = function () {
        $.ajax({
            beforeSend: csrf,
            url: "/add/item",
            type: "GET",
            dataType: "json",
            data: {
                item_id: this.id
            },
            success: setItemForm,
            error: function () {
                console.error(arguments);
            }
        });
    };

    /**
     * request list of names for autocomplete
     *
     * minLength : minimum length required to execute ajax
     * { key : <string> }
     *  response data = [ <name1>, <name2>]
     */
    $(this.donor.input.name).autocomplete({
        source: getNames.bind(this),
        minLength: 2,
        select: getDonorInfo
    });

    $(this.donation.table.tbody).on("click", "tr", function (e) {
        var tr = this.children;
        var data = {};

        data.tax_receipt_no = tr[0].innerText;
        data.donate_date    = tr[1].innerText;
        data.pick_up        = tr[2].innerText;
        data.verified       = tr[3].getElementsByTagName("img")[0].alt;

        setDonationForm(e, data);
        getItems.call(this, data.tax_receipt_no);
        scrollTo(this);
    });

    $(this.item.table.tbody).on("click", "tr", function (e) {
        getItemInfo.call(this);
        scrollTo(this);
    });

    $(this.donor.input.name).on('blur', getDonorInfo);

    $(this.donation.button.addNew).on('click', setDonationForm);
    $(this.donation.button.cancel).on('click', setDonationForm);
    $(this.donation.button.save).on('click', saveDonation);
    $(this.donation.button.update).on('click', function() {});

    $(this.item.button.addNew).on('click', setItemForm);
    $(this.item.button.cancel).on('click', setItemForm);
    $(this.item.button.save).on('click', function() {});
    $(this.item.button.update).on('click', function() {});

    $(this.donor.button.save).on('click', function() {});
    $(this.donor.button.delete).on('click', function() {});
    $(this.donor.button.update).on('click', function() {});

    function scrollTo(id) {
        $('html, body').animate({
            scrollTop: $(id).offset().top + 'px'
        }, 'fast');

        if (id.nodeName == "INPUT") {
            $(id).focus();
        }
    }
}.bind({});

$(function() {
   Form();
});