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


    function defaultError() {
        console.error(arguments);
        alert('Something went wrong. Please refresh the page and try again.');
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

    function setButton(button, type) {
        switch (type) {
            case 'new':
                button.delete.hidden = true;
                button.save.hidden = false;
                button.update.hidden = true;
                if (!!button.addNew) {
                    button.addNew.hidden = true;
                }
                if (!!button.cancel) {
                    button.cancel.hidden = false;
                }
                break;
            case 'existing':
                button.delete.hidden = false;
                button.save.hidden = true;
                button.update.hidden = false;
                if (!!button.addNew) {
                    button.addNew.hidden = true;
                }
                if (!!button.cancel) {
                    button.cancel.hidden = false;
                }
                break;
            default:
                button.delete.hidden = true;
                button.save.hidden = true;
                button.update.hidden = true;
                if (!!button.addNew) {
                    button.addNew.hidden = false;
                }
                if (!!button.cancel) {
                    button.cancel.hidden = true;
                }
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
