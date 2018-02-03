$( function() {

    function log( message ) {
      $( "<div>" ).text( message ).prependTo( "#log" );
      $( "#log" ).scrollTop( 0 );
    }

    $( "#id_donor_name" ).autocomplete({
      source: function( request, response ) {
          $.ajax({
              url: "/add/autocomplete_name",
              dataType: "json",
              data: {
                  key: this.value
              },
              success: function (data) {
                  response(data.result);
              },
              error: function() {
                  console.log(args);
              }
          });
      },
      minLength: 1,
      select: function( event, ui ) {
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
              },
              error: function() {
                  console.log(args);
              }
          });
    }
});