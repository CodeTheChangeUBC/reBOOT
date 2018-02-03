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
                    console.log(arguments);
                }
            });
        },
        minLength: 1,
        select: function (event, ui) {
            setDonor(ui.item.value);
            // console.log( "Selected: " + ui.item.value + " aka " + ui.item.id );
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
                console.log(arguments);
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
                    '    <td class="field-pick_up">'+ donation.pick_up + '</td>\n' +
                    '    <td class="field-verified">' +
                            ((donation.verified) ? '<img src="/static/admin/img/icon-yes.svg" alt="True">' : '<img src="/static/admin/img/icon-no.svg" alt="False">') +
                    '    </td>\n' +
                    '</tr>';
        }

        document.getElementById('donation_result_list').getElementsByTagName("tbody")[0].innerHTML = html;
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
                    console.log(arguments);
                }
            });
    });
});