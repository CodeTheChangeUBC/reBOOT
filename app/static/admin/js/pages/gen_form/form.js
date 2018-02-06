$(function () {
    var _this = this;

    /**
     * Donor form fields
     *
     * REQUIRE: document loaded
     * MODIFIES: this
     * EFFECT: read html node to a variable
     */
    (function (donor) {
        donor.input.name        = document.getElementById('id_donor_name');
        donor.input.email       = document.getElementById('id_email');
        donor.input.telephone   = document.getElementById('id_telephone_number');
        donor.input.mobile      = document.getElementById('id_mobile_number');
        donor.input.ref         = document.getElementById('id_customer_ref');
        donor.input.needReceipt = document.getElementById('id_want_receipt');
        donor.input.address     = document.getElementById('id_address_line');
        donor.input.city        = document.getElementById('id_city');
        donor.input.province    = document.getElementById('id_province');
        donor.input.postalCode  = document.getElementById('id_postal_code');
    }).call(this, this.donor = { input: {} });

    /**
     * Donation table & form fields
     *
     * REQUIRE: document loaded
     * MODIFIES: this
     * EFFECT: read html node to a variable
     */
    (function(donation) {

        donation.div.header         = document.getElementById('donation_header');
        donation.div.form           = document.getElementById('donation_form');

        donation.table.tbody        = document.getElementById('donation_result_list').getElementsByTagName('tbody')[0];

        donation.button.delete      = document.getElementById('btn_delete_donation');
        donation.button.save        = document.getElementById('btn_save_donation');
        donation.button.update      = document.getElementById('btn_update_donation');
        donation.button.addNew      = document.getElementById('btn_add_new_donation');
        donation.button.cancel      = document.getElementById('btn_cancel_donation');

        // note: change of name
        donation.div.taxReceiptNo   = document.getElementById('donation_form').getElementsByClassName('field-tax_receipt_no')[0];

        // note names all change
        // donation.input.name             = document.getElementById('id_donor_name');
        donation.input.taxReceiptNo     = document.getElementById('id_tax_receipt_no');
        donation.input.date             = document.getElementById('id_donate_date');
        donation.input.isVerified       = document.getElementById('id_verified');
        donation.input.pickUpPostalCode = document.getElementById('id_pick_up');
    }).call(this, this.donation = { button : {}, input : {}, div: {}, table: {} });

    /**
     * Items table & form fields
     *
     * REQUIRE: document loaded
     * MODIFIES: this
     * EFFECT: read html node to a variable
     */
    (function(item) {

        item.div.container          = document.getElementById('item_container');
        item.div.header             = document.getElementById('item_header');
        item.div.form               = document.getElementById('item_form');

        item.table.tbody            = document.getElementById('item_result_list').getElementsByTagName('tbody')[0];

        item.button.delete          = document.getElementById('btn_delete_item');
        item.button.save            = document.getElementById('btn_save_item');
        item.button.update          = document.getElementById('btn_update_item');
        item.button.addNew          = document.getElementById('btn_add_new_item');
        item.button.cancel          = document.getElementById('btn_cancel_item');

        item.input.taxReceiptNo     = document.getElementById('id_tax_receipt_no_for_item');
        item.input.itemId           = document.getElementById('id_item_id');
        item.input.description      = document.getElementById('id_description');
        item.input.particulars      = document.getElementById('id_particulars');
        item.input.manufacturer     = document.getElementById('id_manufacturer');
        item.input.model            = document.getElementById('id_model');
        item.input.quantity         = document.getElementById('id_quantity');
        item.input.isWorking        = document.getElementById('id_working');
        item.input.condition        = document.getElementById('id_condition');
        item.input.quality          = document.getElementById('id_quality');
        item.input.isVerified       = document.getElementById('id_item_verified');
        item.input.batch            = document.getElementById('id_batch');
        item.input.value            = document.getElementById('id_value');

    }).call(this, this.item = { button: {}, input: {}, div: {}, table: {}});


    /**
     * REQUIRE: dom variables set
     * MODIFIES: html
     * EFFECT: set form fields with data
     */
    var setDonorForm = function (data) {
        this.email.value       = data.email;
        this.telephone.value   = data.telephone_number;
        this.mobile.value      = data.mobile_number;
        this.ref.value         = data.customer_ref;
        this.needReceipt.value = data.want_receipt;
        this.address.value     = data.address_line;
        this.city.value        = data.city;
        this.province.value    = data.province;
        this.postalCode.value  = data.postal_code;

        printDonationList(data.donation_records);
    }.bind(this.donor.input);

    /**
     * REQUIRE: dom variables set
     * EFFECT: return TRUE if name field is not null
     * @type {function(this:T)}
     */
    var isDonorNamePresent = function() {
        return !(this == '' || this == ' ' || this == null);
    }.bind(this.donor.input.name.value);


    var openNewDonationForm = function () {
        if (!isDonorNamePresent()) {
                alert("Enter donor info first");
                scrollTo(this.donor.input.name);
                return;
        } else {
                this.donation.button.delete.hidden      = true;
                this.donation.button.save.hidden        = false;
                this.donation.button.update.hidden      = true;

                this.donation.div.taxReceiptNo.hidden   = true;

                this.donation.div.header.hidden         = false;
                this.donation.div.header.innerText      = "New Donation";

                printItemList(null);
                scrollTo(this.donation.form);
        }
    }.bind(this);

    /**
     * REQUIRE: dom variables set
     * MODIFIES: dom
     * EFFECT: change button visibilities
     * CLOSURE: true
     */
    var setButton = function(button, type) {
        switch(type) {
            case 'new':
                button.delete.hidden      = true;
                button.save.hidden        = false;
                button.update.hidden      = true;
                button.addNew.hidden      = true;
                button.cancel.hidden      = false;
                break;
            case 'existing':
                button.delete.hidden      = false;
                button.save.hidden        = true;
                button.update.hidden      = false;
                button.addNew.hidden      = true;
                button.cancel.hidden      = false;
                break;
            default:
                button.delete.hidden      = true;
                button.save.hidden        = true;
                button.update.hidden      = true;
                button.addNew.hidden      = false;
                button.cancel.hidden      = true;
        }
    };

    /**
     * REQUIRE: input = { key : dom }
     * MODIFIES: dom
     * EFFECT: reset form fields to null
     */
    var emptyAllFields = function (input) {

        var inputNames = Object.keys(input);
        var ix = inputNames.length;
        var node;

        while(ix--) {

            var node = input[inputNames[ix]];

            if (node.type == 'checkbox') {
                node.checked = false;
                continue;
            }

            node.value = "";
        }
    };

    /**
     * MODIFIES: dom
     * EFFECT: set item form fields
     */
    var setItemForm = function() {
        var _this = this.item;

        return function (data) {
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

    var setDonationForm = function() {

        var _this           = this.donation;
        var donorName       = this.donor.input.name;

        return function (e, data) {

            if (donorName.value == '') {
                alert("Enter donor info first");
                scrollTo(donorName);
                return;
            }

            // [1] event when form closed
            if (this == _this.button.cancel || !e) {
                _this.div.form.hidden = true;
                _this.div.headerhidden = true;

                emptyAllFields(_this.input);
                printItemList(null);
                setButton(_this.button, null);
                return;
            }

            // [2] even when opening form
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
            // [3] even when setting form
            else {
                setButton(_this.button, 'existing');

                _this.div.taxReceiptNo.hidden = false;
                // _this.div.header.hidden = false;
                // _this.div.header.innerText = data.tax_receipt_no;

                _this.input.taxReceiptNo.value      = data.tax_receipt_no || '';
                _this.input.date.value              = data.donate_date || '';
                _this.input.isVerified.checked      = (data.verified == 'true');
                _this.input.pickUpPostalCode.value  = data.pick_up || '';
            }

            _this.div.form.hidden = false;
        };
    }.call(this);


    $(this.donor.input.name).autocomplete({
        source: getNames.bind(this),
        minLength: 2,
        select: requestDonorInfo
    });

    /**
     * request list of names for autocomplete
     *
     * minLength : minimum length required to execute ajax
     * { key : <string> }
     *  response data = [ <name1>, <name2>]
     */
    function getNames (request, response) {
        $.ajax({
            url: "/add/autocomplete_name",
            dataType: "json",
            data: {
                key: this.value
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
    function requestDonorInfo(e, ui) {
        $.ajax({
            url: "/add/get_donor_data",
            dataType: "json",
            data: {
                donor_name: ui.item.value
            },
            success: setDonorForm.bind(_this),
            error: function () {
                console.error(arguments);
            }
        });
    }

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
            scrollTo(donation_result_div);
            donation_table_body.innerHTML = html;
        };
    }();

    var printItemList = function () {
        var _this = this;

        // var item_result_div = document.getElementById('item');
        // var item_table_body = item_result_div.getElementsByTagName('tbody')[0];
        // var header = document.getElementById('item_header');

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

    var saveDonation = function () {
        var form = $(document.getElementById('donation_form').getElementsByTagName('form')[0]);

        return function () {
            $.ajax({
                url: "/add/save_donation_data",
                dataType: "json",
                data: form.serialize(),
                success: printDonationList,
                error: function () {
                    console.error(arguments);
                }
            });
        };
    }();
    var getItems = function () {
        $.ajax({
            url: "/add/get_items",
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
            url: "/add/get_item_data",
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

    $(this.donation.table.tbody).delegate("tr", "click", function (e) {
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

    $(this.item.table.tbody).delegate("tr", "click", function (e) {
        getItemInfo.call(this);
        scrollTo(this);
    });

    // TODO: check if user registered
    $(this.donation.button.addNew).on('click', setDonationForm);
    $(this.donation.button.cancel).on('click', setDonationForm);
    $(this.donation.button.save).on('click', saveDonation);
    // $(this.donation.button.update).on('click', setDonationForm);

    $(this.item.button.addNew).on('click', setItemForm);
    $(this.item.button.cancel).on('click', setItemForm);
    // $(this.item.button.save).on('click', saveDonation);
    // $(this.item.button.update).on('click', saveDonation);


    function scrollTo(id) {
          $('html, body').animate({
            scrollTop: $(id).offset().top + 'px'
        }, 'fast');

          console.log(id.nodeName);
          if (id.nodeName == "INPUT") {
              $(id).focus();
          }
    }
});