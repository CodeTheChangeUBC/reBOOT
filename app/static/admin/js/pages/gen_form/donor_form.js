  const donor_form = new Vue({
    el: '#donor',
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
        <form enctype="multipart/form-data" action="" method="post" id="donor_form" novalidate="">
            <input type="hidden"
                   name="csrfmiddlewaretoken"
                   value="j4wzz67rUvAYQ2vIzFmaYgtv477bXW2bDiAOEdpWe86JFkk0UmctV6TxOQUIM1ab">
            <div>
            <fieldset class="module aligned ">
                    <h2>Donor Contacts</h2>
                    <div class="form-row field-donor_name">
                        <div>
                            <label class="required" for="id_donor_name">Donor Name:</label>
                            <input type="text" name="donor_name" id="id_donor_name" required="" class="vTextField" maxlength="75">
                        </div>
                    </div>
                    <div class="form-row field-email">
                        <div>
                            <label class="required" for="id_email">E-mail:</label>
                            <input type="email" name="email" id="id_email" required="" class="vTextField"
                                   maxlength="254">
                        </div>
                    </div>
                    <div class="form-row field-telephone_number">
                        <div>
                            <label for="id_telephone_number">Telephone #:</label>
                            <input type="text" name="telephone_number" id="id_telephone_number" class="vTextField"
                                   maxlength="30">
                        </div>
                    </div>
                    <div class="form-row field-mobile_number">
                        <div>
                            <label for="id_mobile_number">Mobile #:</label>
                            <input type="text" name="mobile_number" id="id_mobile_number" class="vTextField"
                                   maxlength="30">
                        </div>
                    </div>
                    <div class="form-row field-customer_ref">
                        <div>
                            <label for="id_customer_ref">Customer Ref.</label>
                            <input type="text" name="customer_ref" id="id_customer_ref" class="vTextField"
                                   maxlength="20">
                        </div>
                    </div>
                </fieldset>
                <fieldset class="module aligned ">
                    <h2>Details</h2>
                    <div class="form-row field-want_receipt">
                        <div class="checkbox-row">
                            <input type="checkbox" name="want_receipt" id="id_want_receipt"><label
                                class="vCheckboxLabel" for="id_want_receipt">Tax receipt?</label>
                        </div>
                    </div>
                </fieldset>
                <fieldset class="module aligned ">
                    <h2>Address</h2>
                    <div class="form-row field-address_line">
                        <div>
                            <label class="required" for="id_address_line">Street Address:</label>
                            <input type="text" name="address_line" id="id_address_line" required="" class="vTextField"
                                   maxlength="256">
                        </div>
                    </div>
                    <div class="form-row field-city">
                        <div>
                            <label class="required" for="id_city">City:</label>
                            <input type="text" name="city" id="id_city" required="" class="vTextField" maxlength="30">
                        </div>
                    </div>
                    <div class="form-row field-province">
                        <div>
                            <label class="required" for="id_province">Province:</label>
                            <select name="province" required="" id="id_province">
                                <option value="" selected="">---------</option>
                                <option value="AB">Alberta</option>
                                <option value="BC">British Columbia</option>
                                <option value="ON">Ontario</option>
                                <option value="NS">Nova Scotia</option>
                                <option value="NL">Newfoundland and Labrador</option>
                                <option value="SK">Saskatchewan</option>
                                <option value="YT">Yukon</option>
                                <option value="MB">Manitoba</option>
                                <option value="NU">Nunavut</option>
                                <option value="PE">Prince Edward Island</option>
                                <option value="NT">Northwest Territories</option>
                                <option value="QC">Quebec</option>
                                <option value="NB">New Brunswick</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row field-postal_code">
                        <div>
                            <label class="required" for="id_postal_code">Postal Code:</label>
                            <input type="text" name="postal_code" id="id_postal_code" required="" class="vTextField"
                                   maxlength="7">
                        </div>
                    </div>
                </fieldset>
                <div class="submit-row">
                    <input type="submit" value="Save" class="default" name="_save">
                </div>
            </div>
        </form>
    </div>
    `,
});
