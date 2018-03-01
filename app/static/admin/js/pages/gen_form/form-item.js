define(
  ["./form-util"],
  function(util) {
    /**
     * Items table & form fields
     */
    this.dom = {
      div: {
        container: document.getElementById("item_container"),
        header: document.getElementById("item_header"),
        form: document.getElementById("item_form")
      },
      table: {
        tbody: document
          .getElementById("item_result_list")
          .getElementsByTagName("tbody")[0]
      },
      button: {
        delete: document.getElementById("btn_delete_item"),
        save: document.getElementById("btn_save_item"),
        update: document.getElementById("btn_update_item"),
        addNew: document.getElementById("btn_add_new_item"),
        cancel: document.getElementById("btn_cancel_item")
      },
      input: {
        taxReceiptNo: document.getElementById("id_tax_receipt_no_for_item"),
        itemId: document.getElementById("id_item_id"),
        description: document.getElementById("id_description"),
        particulars: document.getElementById("id_particulars"),
        manufacturer: document.getElementById("id_manufacturer"),
        model: document.getElementById("id_model"),
        quantity: document.getElementById("id_quantity"),
        isWorking: document.getElementById("id_working"),
        condition: document.getElementById("id_condition"),
        quality: document.getElementById("id_quality"),
        isVerified: document.getElementById("id_item_verified"),
        batch: document.getElementById("id_batch"),
        value: document.getElementById("id_value")
      }
    };

    var setItemForm = function() {
      var _this = this.dom;
      // var donorName       = this.donor.input.name;

      return function(data) {
        // [*]
        if (this == _this.button.addNew && !util.isDonorNamePresent) {
          util.enterDonorName();
          return;
        }

        if (!data) {
          util.emptyAllFields(_this.input);
          _this.div.form.hidden = true;
          util.setButton(_this.button, null);

          return;
        }

        if (this == _this.button.cancel) {
          util.emptyAllFields(_this.input);
          _this.div.form.hidden = true;
          util.setButton(_this.button, null);

          return;
        }

        if (this == _this.button.addNew) {
          util.emptyAllFields(_this.input);
          _this.div.form.hidden = false;
          util.setButton(_this.button, "new");
          util.scrollTo(_this.input.description);

          return;
        }

        if (this == _this.button.cancel) {
          util.emptyAllFields(_this.input);
          _this.div.form.hidden = true;
          util.setButton(_this.button, null);

          return;
        }

        // TODO item id
        _this.input.taxReceiptNo.value = data.taxReceiptNo;
        _this.input.itemId.value = data.itemId;
        _this.input.description.value = data.description;
        _this.input.particulars.value = data.particulars;
        _this.input.manufacturer.value = data.manufacturer;
        _this.input.model.value = data.model;
        _this.input.quantity.value = data.quantity;
        _this.input.isWorking.checked = data.isWorking;
        _this.input.condition.value = data.condition;
        _this.input.quality.value = data.quality;
        _this.input.isVerified.checked = data.isVerified;
        _this.input.batch.value = data.batch;
        _this.input.value.value = data.value;

        _this.div.form.hidden = false;
        util.setButton(_this.button, "existing");
      };
    }.call(this);

    var printItemList = function() {
      var _this = this;

      return function(data) {
        if (!data) {
          _this.div.container.hidden = true;
          setItemForm(null);
          return;
        }

        _this.div.container.hidden = false;
        _this.div.header.value = this.id; // tax_receipt_no;

        var html = "";
        var item;
        for (var ix = 0, ixLen = data.length; ix < ixLen; ix++) {
          item = data[ix];
          html +=
            '<tr class="row' +
            (ix % 2 ? 2 : 1) +
            '" id="' +
            item.item_id +
            '" >\n' +
            // '                        <td class="action-checkbox"><input type="checkbox" name="_selected_action" value='+item.item_id +'\n' +
            // '                                                           class="action-select"></td>\n' +
            '<td class="field-get_item">' +
            item.item_id +
            "</td>\n" +
            '<td class="field-manufacturer">' +
            item.manufacturer +
            "</td>\n" +
            '<td class="field-model">' +
            item.model +
            "</td>\n" +
            '<td class="field-quantity">' +
            item.quantity +
            "</td>\n" +
            '<td class="field-batch">' +
            item.batch +
            "</td>\n" +
            '<td class="field-verified">' +
            (item.verified
              ? '<img src="/static/admin/img/icon-yes.svg" alt=true>'
              : '<img src="/static/admin/img/icon-no.svg" alt=false>') +
            "</td>\n" +
            "</tr>";
        }

        setItemForm(null);
        util.setButton(_this.button, null);
        // scrollTo(item_result_div);
        _this.table.tbody.innerHTML = html;
      };
    }.call(this.dom);

    var getItemInfo = function() {
      $.ajax({
        beforeSend: util.csrf,
        url: "/api/item",
        type: "GET",
        dataType: "json",
        data: {
          item_id: this.id
        },
        success: setItemForm,
        error: function() {
          console.error(arguments);
        }
      });
    };

    var getItems = function() {
      $.ajax({
        beforeSend: util.csrf,
        url: "/api/item",
        type: "GET",
        dataType: "json",
        data: {
          tax_receipt_no: this.id
        },
        success: printItemList.bind(this),
        error: function() {
          console.error(arguments);
        }
      });
    };

    $(this.dom.table.tbody).on("click", "tr", function(e) {
      getItemInfo.call(this);
      scrollTo(this);
    });

    $(this.dom.button.addNew).on("click", setItemForm);
    $(this.dom.button.cancel).on("click", setItemForm);
    $(this.dom.button.save).on("click", function() {});
    $(this.dom.button.update).on("click", function() {});

    return {
      printItemList: printItemList,
      getItemInfo: getItemInfo,
      getItems: getItems
    };
  }.bind({})
);
