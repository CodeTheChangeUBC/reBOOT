define(function() {

    var cookie = function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }('csrftoken');

    var set = function() {
        this._ = this._ || {};
        var _ = this._;
        return function(key, value) {
            _[key] = value;
        };
    }();

    var get = function(key) {
        return this._[key];
    }.bind(this._);

    var check = function () {
        var _ = this._;
        return function(key, value) {
            if (_[key] == undefined || _[key] != value) {
                set(key, value);
                return false;
            }
            return true;
        }
    }();
    var scrollTo = function (id) {
        $('html, body').animate({
            scrollTop: $(id).offset().top + 'px'
        }, 'fast');

        if (id.nodeName == "INPUT") {
            $(id).focus();
        }
    };
    var donorName = document.getElementById("id_donor_name");

    var isDonorNamePresent = function () {
        return donorName.value != null && donorName.value != "" && donorName.value != /\s+/;
    };

    var enterDonorName = function() {
        alert("Enter donor info first");
        scrollTo(donorName);
    };

    return {
        setButton : function(button, type) {
            switch(type) {
                case 'new':
                    button.delete.hidden      = true;
                    button.save.hidden        = false;
                    button.update.hidden      = true;
                    button.addNew? button.addNew.hidden = true  : null;
                    button.cancel? button.cancel.hidden = false : null;
                    break;
                case 'existing':
                    button.delete.hidden      = false;
                    button.save.hidden        = true;
                    button.update.hidden      = false;
                    button.addNew? button.addNew.hidden = true  : null;
                    button.cancel? button.cancel.hidden = false : null;
                    break;
                default:
                    button.delete.hidden      = true;
                    button.save.hidden        = true;
                    button.update.hidden      = true;
                    button.addNew? button.addNew.hidden = false : null;
                    button.cancel? button.cancel.hidden = true  : null;
            }
        },
        emptyAllFields: function (input, exceptions) {
            var inputNames = Object.keys(input);
            var ix = inputNames.length;
            var node;

            while(ix--) {
                node = input[inputNames[ix]];

                if (exceptions && exceptions.includes && exceptions.includes(node)) {
                    continue;
                }

                if (node.type == 'checkbox') {
                    node.checked = false;
                    continue;
                }

                node.value = "";
            }
        },

        csrf : function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {// Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", cookie);
            }
        },
        scrollTo: scrollTo,
        set: set,
        check: check,
        isDonorNamePresent: isDonorNamePresent,
        enterDonorName: enterDonorName,
    }
});