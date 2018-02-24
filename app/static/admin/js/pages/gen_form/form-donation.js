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

    var setDonationForm = function() {
      var _this = this.dom;

      return function(e, data) {
        // [*]
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
          item.printItemList(null);
          util.setButton(_this.button, "new");
          _this.div.form.hidden = false;

          _this.div.taxReceiptNo.hidden = true;
          util.scrollTo(_this.input.date);
          return;
        }

        // [1] event when form needs to be closed
        if (this == _this.button.cancel || !data) {
          _this.div.form.hidden = true;
          _this.div.header.hidden = true;

          util.emptyAllFields(_this.input);
          item.printItemList(null);
          util.setButton(_this.button, null);
          return;
        } else {
          // [3] event to set form with data
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
        for (var ix = 0, ixLen = data.length; ix < ixLen; ix++) {
          donation = data[ix];
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
      $.ajax({
        beforeSend: util.csrf,
        url: "/api/donation",
        type: "POST",
        dataType: "json",
        data: this.serialize(),
        success: printDonationList,
        error: function() {
          console.error(arguments);
        }
      });
    }.bind(this.dom.form);

    $(this.dom.table.tbody).on("click", "tr", function(e) {
      var tr = this.children;
      var data = {};

      data.tax_receipt_no = tr[0].innerText;
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
      printDonationList: printDonationList
    };
  }.bind({})
);
