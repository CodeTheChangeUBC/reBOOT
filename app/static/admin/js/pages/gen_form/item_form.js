  const item_form = new Vue({
    el: '#item',
    data: {
      editFriend: null,
      friends: [],
    },
    methods: {
      deleteFriend(id, i) {
        fetch("http://rest.learncode.academy/api/vue-5/friends/" + id, {
          method: "DELETE"
        })
        .then(() => {
          this.friends.splice(i, 1);
        })
      },
      updateFriend(friend) {
        fetch("http://rest.learncode.academy/api/vue-5/friends/" + friend.id, {
          body: JSON.stringify(friend),
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then(() => {
          this.editFriend = null;
        })
      }
    },
    mounted() {
      fetch("http://rest.learncode.academy/api/vue-5/friends")
        .then(response => response.json())
        .then((data) => {
          this.friends = data;
        })
    },
    template: `
    <div id="content-main">
        <form enctype="multipart/form-data" action="" method="post" id="item_form" novalidate="">
            <input type="hidden" name="csrfmiddlewaretoken" value="77a6dhyCcTQJW9kq6jJFmathyBaIdH3orlelioQ7wwmuLr9Ir0zYj0TjikXf2Mbo">
            <div>
                <fieldset class="module aligned ">
                    <h2>Item</h2>
                    <div class="form-row field-tax_receipt_no">
                        <div>
                            <label class="required" for="id_tax_receipt_no">Tax Receipt Number:</label>
                            <div class="related-widget-wrapper">
                                <select name="tax_receipt_no" required="" id="id_tax_receipt_no">
                                    <option value="" selected="">---------</option>
                                </select>
                                <a class="related-widget-wrapper-link change-related" id="change_id_tax_receipt_no"
                                   data-href-template="/app/donation/__fk__/change/?_to_field=tax_receipt_no&amp;_popup=1"
                                   title="Change selected donation"><img src="/static/admin/img/icon-changelink.svg"
                                                                         alt="Change"></a><a
                                    class="related-widget-wrapper-link add-related" id="add_id_tax_receipt_no"
                                    href="/app/donation/add/?_to_field=tax_receipt_no&amp;_popup=1"
                                    title="Add another donation"><img src="/static/admin/img/icon-addlink.svg"
                                                                      alt="Add"></a>
                            </div>
                        </div>
                    </div>
                    <div class="form-row field-description">
                        <div>
                            <label for="id_description">Description:</label>
                            <input type="text" name="description" id="id_description" class="vTextField"
                                   maxlength="500">
                        </div>
                    </div>
                    <div class="form-row field-particulars">
                        <div>
                            <label for="id_particulars">Particulars:</label>
                            <input type="text" name="particulars" id="id_particulars" class="vTextField" maxlength="500">
                        </div>
                    </div>
                    <div class="form-row field-manufacturer">
                        <div>
                            <label for="id_manufacturer">Manufacturer:</label>
                            <input type="text" name="manufacturer" id="id_manufacturer" class="vTextField" maxlength="500">
                        </div>
                    </div>
                    <div class="form-row field-model">
                        <div>
                            <label for="id_model">Model:</label>
                            <input type="text" name="model" id="id_model" class="vTextField" maxlength="50">
                        </div>
                    </div>
                    <div class="form-row field-quantity">
                        <div>
                            <label class="required" for="id_quantity">Quantity:</label>
                            <input type="number" name="quantity" required="" class="vIntegerField" id="id_quantity">
                        </div>
                    </div>
                    <div class="form-row field-working">
                        <div class="checkbox-row">
                            <input type="checkbox" name="working" id="id_working">
                            <label class="vCheckboxLabel" for="id_working">Is the item working?</label>
                        </div>
                    </div>
                    <div class="form-row field-condition">
                        <div>
                            <label for="id_condition">Condition:</label>
                            <input type="text" name="condition" id="id_condition" class="vTextField" maxlength="20">
                        </div>
                    </div>
                    <div class="form-row field-quality">
                        <div>
                            <label class="required" for="id_quality">Quality:</label>
                            <select name="quality" required="" id="id_quality">
                                <option value="" selected="">---------</option>
                                <option value="H">High</option>
                                <option value="L">Low</option>
                                <option value="M">Medium</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row field-verified">
                        <div class="checkbox-row">
                            <input type="checkbox" name="verified" id="id_verified">
                            <label class="vCheckboxLabel" for="id_verified">Verified Item</label>
                        </div>
                    </div>
                    <div class="form-row field-batch">
                        <div>
                            <label for="id_batch">Batch:</label>
                            <input type="text" name="batch" id="id_batch" class="vTextField" maxlength="20">
                        </div>
                    </div>
                    <div class="form-row field-value">
                        <div>
                            <label for="id_value">Value:</label>
                            <input type="number" name="value" value="0" step="0.01" id="id_value">
                        </div>
                    </div>
                </fieldset>
                <div class="submit-row">
                    <input type="submit" value="Save" class="default" name="_save">
                    <input type="submit" value="Save and add another" name="_addanother">
                    <input type="submit" value="Save and continue editing" name="_continue">
                </div>
            </div>
        </form>
    </div>
    `,
});
