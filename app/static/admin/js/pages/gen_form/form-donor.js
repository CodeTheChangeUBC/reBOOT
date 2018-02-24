define(
  ["./form-util", "./form-donation", "./form-item"],
  function(util, donation, item) {
    /**
     * Donor form fields
     */
    this.dom = {
      button: {
        delete: document.getElementById("btn_delete_donor"),
        save: document.getElementById("btn_save_donor"),
        update: document.getElementById("btn_update_donor")
      },
      input: {
        name: document.getElementById("id_donor_name"),
        email: document.getElementById("id_email"),
        telephone: document.getElementById("id_telephone_number"),
        mobile: document.getElementById("id_mobile_number"),
        ref: document.getElementById("id_customer_ref"),
        needReceipt: document.getElementById("id_want_receipt"),
        address: document.getElementById("id_address_line"),
        city: document.getElementById("id_city"),
        province: document.getElementById("id_province"),
        postalCode: document.getElementById("id_postal_code")
      }
    };

    var getDonorInfo = function(e, ui) {
      var value = (ui && ui.item && ui.item.value) || e.target.value;

      if (!value || value == "") {
        setDonorForm.apply(null, null);
        return;
      }

      if (util.check("name", value)) return;

      $.ajax({
        type: "GET",
        url: "/api/donor",
        dataType: "json",
        data: {
          donor_id: 127 // TODO: Change to real donor_id
        },
        success: function() {
          setDonorForm.apply(null, arguments);
        },
        error: function() {
          console.error(arguments);
        }
      });
    }.bind(this);

    var setDonorForm = function(data) {
      if (!data) {
        util.emptyAllFields(this.input, [this.input.name]);
        util.setButton(this.button, "new");
        donation.printDonationList([]);
        return;
      }

      this.input.email.value = data.email;
      this.input.telephone.value = data.telephone_number;
      this.input.mobile.value = data.mobile_number;
      this.input.ref.value = data.customer_ref;
      this.input.needReceipt.value = data.want_receipt;
      this.input.address.value = data.address_line;
      this.input.city.value = data.city;
      this.input.province.value = data.province;
      this.input.postalCode.value = data.postal_code;

      util.setButton(this.button, "existing");
      donation.printDonationList(data.donation_records);
    }.bind(this.dom);

    /**
     * REQUIRE: this.donor.input.name == name field
     * EFFECT: calls for a list of names
     */
    function getNames(request, response) {
      $.ajax({
        url: "/api/autocomplete_name",
        dataType: "json",
        data: {
          key: this.dom.input.name.value
        },
        success: function(data) {
          response(data);
        },
        error: function() {
          console.error(arguments);
        }
      });
    }

    /**
     * request list of names for autocomplete
     *
     * minLength : minimum length required to execute ajax
     * { key : <string> }
     *  response data = [ <name1>, <name2>]
     */
    $(this.dom.input.name).autocomplete({
      source: getNames.bind(this),
      minLength: 2,
      select: getDonorInfo
    });

    $(this.dom.input.name).on("blur", getDonorInfo);
    $(this.dom.button.save).on("click", function() {});
    $(this.dom.button.delete).on("click", function() {});
    $(this.dom.button.update).on("click", function() {});

    return {};
  }.bind({})
);
