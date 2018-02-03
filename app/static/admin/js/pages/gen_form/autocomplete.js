$(function () {

    function log(message) {
        $("<div>").text(message).prependTo("#log");
        $("#log").scrollTop(0);
    }

    $("#id_donor_name").autocomplete({
        source: function (request, response) {
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
        },
        minLength: 1,
        select: function (event, ui) {
            setDonor(ui.item.value);
        }
    });

    function setDonor(donorName) {
        $.ajax({
            url: "/add/get_donor_data",
            dataType: "json",
            data: {
                id_donor_name: donorName
            },
            success: function (data) {
                $('#id_email').val(data.id_email);
                $('#id_telephone_numb').val(data.id_telephone_numb);
                $('#id_mobile_number').val(data.id_mobile_number);
                $('#id_customer_ref').val(data.id_customer_ref);
                $('#id_want_receipt').val(data.id_want_receipt);
                $('#id_address_line').val(data.id_address_line);
                $('#id_city').val(data.id_city);
                $('#id_province').val(data.id_province);
                $('#id_postal_code').val(data.id_postal_code);

                printDonationList(data.donation_records);
            },
            error: function () {
                console.error(arguments);
            }
        });
    }

    /*
                "/app/donation/2017-0223/change/"
    * */
    function printDonationList(data) {
        var html = '';
        var donation;
        for (var ix = 0, ixLen = data.length; ix < ixLen; ix++) {
            donation = data[ix];

            html += '<tr class="row' + ((ix % 2) ? 2 : 1) + '" id="' + donation.tax_receipt_no + '" >\n' +
                '    <td class="field-tax_receipt_no">' + donation.tax_receipt_no + '</td>\n' +
                '    <td class="field-donate_date nowrap">' + donation.donate_date + '</td>\n' +
                '    <td class="field-pick_up">' + donation.pick_up + '</td>\n' +
                '    <td class="field-verified">' +
                ((donation.verified) ? '<img src="/static/admin/img/icon-yes.svg" alt="True">' : '<img src="/static/admin/img/icon-no.svg" alt="False">') +
                '    </td>\n' +
                '</tr>';
        }

        document.getElementById('donation_result_list').getElementsByTagName("tbody")[0].innerHTML = html;

        $('html, body').animate({
            scrollTop: $("#donation_result_list").offset().top + 'px'
        }, 'fast');
    }

    $("#donation_result_list").delegate("tr", "click", function () {
        $.ajax({
            url: "/add/get_donation_data",
            dataType: "json",
            data: {
                tax_receipt_no: this.id
            },
            success: function (data) {
                console.log(data.result);
            },
            error: function () {
                console.error(arguments);
            }
        });

        this.append(

        );
    });

    $('#btn_add_new_donation').on('click', function () {
        // show empty form without receipt number
        document.getElementById('donation_form').hidden = false;
        document.getElementById('btn_add_new_donation').hidden = true;
        document.getElementById('btn_save_donation').hidden = false;
        document.getElementById('donation_form').getElementsByClassName('field-tax_receipt_no')[0].hidden = true;
        document.getElementById('btn_delete_donation').hidden = true;

        $('html, body').animate({
            scrollTop: $("#donation_form").offset().top + 'px'
        }, 'fast');
    });

    $('#btn_save_donation').on('click', function () {
        // show empty form without receipt number
        var form = $(document.getElementById('donation_form').getElementsByTagName('form')[0]);

        $.ajax({
            url: "/add/save_donation_data",
            dataType: "json",
               data: {
                donation_data: JSON.stringify(form.serializeArray())
            },
            success: function (data) {
                printDonationList(data.donation_records);

                document.getElementById('donation_form').hidden = true;
                document.getElementById('btn_add_new_donation').hidden = false;
                document.getElementById('btn_save_donation').hidden = true;
            },
            error: function () {
                console.error(arguments);
            }
        });
    });
});