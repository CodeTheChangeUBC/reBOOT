"use strict";
define(function() {

    var cookie = (function(name) {
        var cookieValue = null;
        if (!!document.cookie) {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }('csrftoken'));

    function csrf(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) { // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", cookie);
        }
    }

    function scrollTo(id) {
        $('html, body').animate({
            scrollTop: $(id).offset().top + 'px'
        }, 'fast');
        if (id.nodeName === "INPUT") {
            $(id).focus();
        }
    }

    var donorName = document.getElementById("id_donor_name");

    function isDonorNamePresent() {
        return !!donorName.value && donorName.value !== /\s+/;
    }

    function enterDonorName() {
        alert("Enter donor info first");
        scrollTo(donorName);
    }

    function friendlyErrors(request) {
        var errors = [];
        if (request.responseJSON) {
            errors = request.responseJSON.errors;
        }
        return errors;
    }


    function defaultError(request) {
        var errors = friendlyErrors(request);
        if (errors.length > 0) {
            alert(errors.join(" "));
        } else {
            console.error(arguments);
            alert('Something went wrong. The page will now reload. Please try again.');
        }
        location.reload();
    }

    function ajax(param) {
        $.ajax({
            beforeSend: csrf,
            url: param.url,
            type: param.type || "GET",
            dataType: "json",
            data: param.data,
            success: param.success,
            error: param.error || defaultError
        });
    }

    /**
     * Empty function used for param defaulting
     */
    var noop = function() {};

    function serializeObject(element) {
        var data = $(element).serializeArray();
        var obj = {};
        for (var i = 0; i < data.length; i++) {
            obj[data[i].name] = data[i].value;
        }
        return obj;
    }

    function setButtonValue(button, val) {
        if (!!button) {
            button.hidden = val;
        }
    }

    function setButton(button, type) {
        switch (type) {
            case 'new':
                setButtonValue(button.delete, true);
                setButtonValue(button.save, false);
                setButtonValue(button.update, true);
                setButtonValue(button.addNew, true);
                setButtonValue(button.cancel, false);
                break;
            case 'existing':
                setButtonValue(button.delete, false);
                setButtonValue(button.save, true);
                setButtonValue(button.update, false);
                setButtonValue(button.addNew, true);
                setButtonValue(button.cancel, false);
                break;
            default:
                setButtonValue(button.delete, true);
                setButtonValue(button.save, true);
                setButtonValue(button.update, true);
                setButtonValue(button.addNew, false);
                setButtonValue(button.cancel, true);
        }
    }

    function emptyAllFields(input, exceptions) {
        var inputNames = Object.keys(input);
        var ix = inputNames.length;
        var node;

        while (ix--) {
            node = input[inputNames[ix]];

            if (exceptions && exceptions.includes && exceptions.includes(node)) {
                continue;
            }

            if (node.type === 'checkbox') {
                node.checked = false;
                continue;
            }

            node.value = "";
        }
    }

    return {
        setButton: setButton,
        emptyAllFields: emptyAllFields,
        scrollTo: scrollTo,
        isDonorNamePresent: isDonorNamePresent,
        enterDonorName: enterDonorName,
        ajax: ajax,
        noop: noop,
        serializeObject: serializeObject
    };
});
