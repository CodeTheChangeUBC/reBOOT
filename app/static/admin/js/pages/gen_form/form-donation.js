define(
  ["./form-util", "./form-item"],
  function(util, item) {
    /**
     * Donation table & form fields
     */
    this.dom = {
      div: {
        header: document.getElementById("donation_header"),
        form: document.getElementById("donation_form"),
        taxReceiptNo: document
          .getElementById("donation_form")
          .getElementsByClassName("field-tax_receipt_no")[0]
      },
      form: $(
        document.getElementById("donation_form").getElementsByTagName("form")[0]
      ),
      table: {
        tbody: document
          .getElementById("donation_result_list")
          .getElementsByTagName("tbody")[0]
      },
      button: {
        delete: document.getElementById("btn_delete_donation"),
        save: document.getElementById("btn_save_donation"),
        update: document.getElementById("btn_update_donation"),
        addNew: document.getElementById("btn_add_new_donation"),
        cancel: document.getElementById("btn_cancel_donation")
      },
      input: {
        taxReceiptNo: document.getElementById("id_tax_receipt_no"),
        date: document.getElementById("id_donate_date"),
        isVerified: document.getElementById("id_verified"),
        pickUpPostalCode: document.getElementById("id_pick_up")
      }
    };

    var store = {};
    var getDonation = function(id) {
      if (id == null) {
        printDonationList([]);
        return;
      }

      $.ajax({
        type: "GET",
        url: "/api/donation",
        dataType: "json",
        data: {
          donor_id: id // TODO: Change to real donor_id
        },
        success: printDonationList,
        //   function(data, textStatus, jqXHR) {
        //   store = {};
        //   data.reduce(function(store, donation) {
        //         store[donation.donor_id] = donation;
        //         return store;
        //   }, store);
        //
        //   printDonationList.apply(null, argu);
        // },
        error: function() {
          console.error(arguments);
        }
      });

      // donation.printDonationList(data.donation_records);
    };

    var setDonationForm = function() {
      var _this = this.dom;

      return function(e, data) {
        // [1] donor name not present
        if (this == _this.button.addNew && !util.isDonorNamePresent()) {
          util.enterDonorName();
          return;
        }

        // [2] event to open an empty form
        if (this == _this.button.addNew) {
          // _this.div.header.hidden = false;
          // _this.div.header.innerText = "New Donation";

          // TODO set donor id to the form

          util.emptyAllFields(_this.input);
          item.clearItemList();
          util.setButton(_this.button, "new");
          _this.div.form.hidden = false;

          _this.div.taxReceiptNo.hidden = true;
          util.scrollTo(_this.input.date);
          return;
        }

        // [3] event when form needs to be closed
        if (this == _this.button.cancel || !data) {
          _this.div.form.hidden = true;
          _this.div.header.hidden = true;

          util.emptyAllFields(_this.input);
          item.clearItemList();
          util.setButton(_this.button, null);
          return;
        } else {
          // [4] event to set form with data

          //
          if (!util.check('tax_receipt_no', data.tax_receipt_no)) return;

          util.setButton(_this.button, "existing");

          _this.div.taxReceiptNo.hidden = false;
          // _this.div.header.hidden = false;
          // _this.div.header.innerText = data.tax_receipt_no;

          _this.input.taxReceiptNo.value = data.tax_receipt_no || "";
          _this.input.date.value = data.donate_date || "";
          _this.input.isVerified.checked =
            data.verified.toUpperCase() == "TRUE";
          _this.input.pickUpPostalCode.value = data.pick_up || "";
        }

        _this.div.form.hidden = false;
      };
    }.call(this);

    var printDonationList = (function() {
      var donation_result_div = document.getElementById("donation_result_list");
      var donation_table_body = donation_result_div.getElementsByTagName(
        "tbody"
      )[0];

      return function(data) {
        var html = "";
        var donation;
        // store = {};
        for (var ix = 0; data && ix < data.length; ix++) {
          donation = data[ix];
          // store[donation.donor_id] = donation;
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

        setDonationForm.call(this, null);
        // scrollTo(donation_result_div);
        donation_table_body.innerHTML = html;
      };
    })();

    var saveDonation = function() {
      console.log(this.serialize());
      $.ajax({
        beforeSend: util.csrf,
        url: "/api/donation",
        type: "POST",
        dataType: "json",
        data: {
          donor_id: 127
        },
        success: function(response) {
          console.log("Response", response);
        },
        error: function() {
          console.error(arguments);
        }
      });
    }.bind(this.dom.form);

    function isSameAsCurrent(tax_receipt_no) {
      return util.check('tax_receipt_no', tax_receipt_no);
    }

    $(this.dom.table.tbody).on("click", "tr", function(e) {
      var tr = this.children;
      var data = {};

      data.tax_receipt_no = tr[0].innerText;
      if (isSameAsCurrent(data.tax_receipt_no)) return;
      data.donate_date = tr[1].innerText;
      data.pick_up = tr[2].innerText;
      data.verified = tr[3].getElementsByTagName("img")[0].alt;

      setDonationForm(e, data);
      item.getItems.call(this, data.tax_receipt_no);
      util.scrollTo(this);
    });
    $(this.dom.button.addNew).on("click", setDonationForm);
    $(this.dom.button.cancel).on("click", setDonationForm);
    $(this.dom.button.save).on("click", saveDonation);
    $(this.dom.button.update).on("click", function() {});

    return {
      printDonationList: printDonationList,
      getDonation: getDonation
    };
  }.bind({})
);
