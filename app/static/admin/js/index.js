 function upload(event) {
        event.preventDefault();

        var data = new FormData($('#csv_form')[0]);
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        console.log(data);

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            enctype: $(this).attr('enctype'),
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(data) {
                alert('success');
            }
        });

        alert('Your file has been submitted. Please wait');
        return false;
    }

    $(function() {
        $('#csv_form').submit(upload);
    });