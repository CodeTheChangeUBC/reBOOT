const donation_form = new Vue({
    el: '#donation',
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
        <form enctype="multipart/form-data" action="" method="post" id="donation_form" novalidate="">
            <input type="hidden" name="csrfmiddlewaretoken" value="8D6ymWMuIJXgupCxPMb9AfnPxKJG874DsRaNr34Z2mt1jHrPat1sx5NRhtwdXccD">
            <div>
                <fieldset class="module aligned ">
                    <h2>Donation</h2>
                    <div class="form-row field-donor_id">
                        <div>
                            <label class="required" for="id_donor_id">Donor ID:</label>
                            <select name="donor_id" required="" id="id_donor_id">
                                <option value="" selected="">---------</option>
                                <option value="1">1</option>
                                <option value="2">2</option>
                                <option value="3">3</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row field-get_donation_donor_name">
                        <div>
                            <label class="required">Donor Name:</label>
                            <input type="text" id="donor_name" class="vTextField">
                        </div>
                    </div>
                    <div class="form-row field-tax_receipt_no">
                        <div>
                            <label class="required" for="id_tax_receipt_no">Tax Receipt Number:</label>
                            <input type="text" name="tax_receipt_no" id="id_tax_receipt_no" required="" class="vTextField" maxlength="9">
                        </div>
                    </div>
                    <div class="form-row field-donate_date">
                        <div>
                            <label class="required" for="id_donate_date">Date Donated:</label>
                            <input type="text" name="donate_date" id="id_donate_date" required="" class="vDateField" size="10">
                        </div>
                    </div>
                    <div class="form-row field-verified">
                        <div class="checkbox-row">
                            <input type="checkbox" name="verified" id="id_verified">
                            <label class="vCheckboxLabel" for="id_verified">
                                Verified Donation
                            </label>
                        </div>
                    </div>
                    <div class="form-row field-pick_up">
                        <div>
                            <label for="id_pick_up">Pick-Up Postal:</label>
                            <input type="text" name="pick_up" id="id_pick_up" class="vTextField" maxlength="30">
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