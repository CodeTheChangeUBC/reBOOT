/*global define, alert, $*/
"use strict";
define(function() {
  function cookie(name) {
    name = name || 'csrftoken';
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
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
  }

  var set = function(key, value) {
    this._ = this._ || {};
    this._[key] = value;
  };

  var get = function(key) {
    return this._[key];
  }.bind(this._);

  var check = function(key, value) {
    var _ = this._;
    if (_[key] === undefined || _[key] !== value) {
      set(key, value);
      return false;
    }
    return true;
  };
  var scrollTo = function(id) {
    $('html, body').animate({
      scrollTop: $(id).offset().top + 'px'
    }, 'fast');

    if (id.nodeName === "INPUT") {
      $(id).focus();
    }
  };

  var isDonorNamePresent = function() {
    var donorName = $("#id_donor_name");
    return donorName.value !== null && donorName.value !== "" && donorName.value !== /\s+/;
  };

  var enterDonorName = function() {
    alert("Enter donor info first");
    var donorName = $("#id_donor_name");
    scrollTo(donorName);
  };

  var csrf = function(xhr, settings) {
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) { // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", cookie);
    }
  };

  var ajax = function(param) {
    $.ajax({
      beforeSend: csrf,
      url: param.url,
      type: param.type || "GET",
      dataType: "json",
      data: param.data,
      success: param.success,
      error: param.error
    });
  };

  var emptyAllFields = function(input, exceptions) {
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
  };

  var setButton = function(button, type) {
    switch (type) {
      case 'new':
        button.delete.hidden = true;
        button.save.hidden = false;
        button.update.hidden = true;
        button.addNew ? button.addNew.hidden = true : null;
        button.cancel ? button.cancel.hidden = false : null;
        break;
      case 'existing':
        button.delete.hidden = false;
        button.save.hidden = true;
        button.update.hidden = false;
        button.addNew ? button.addNew.hidden = true : null;
        button.cancel ? button.cancel.hidden = false : null;
        break;
      default:
        button.delete.hidden = true;
        button.save.hidden = true;
        button.update.hidden = true;
        button.addNew ? button.addNew.hidden = false : null;
        button.cancel ? button.cancel.hidden = true : null;
    }
  };

  function somethingWentWrong() {
    console.error(arguments);
    alert('Something went wrong. Please refresh the page and try again.');
  }

  return {
    setButton: setButton,
    emptyAllFields: emptyAllFields,
    csrf: csrf,
    scrollTo: scrollTo,
    get: get,
    set: set,
    check: check,
    isDonorNamePresent: isDonorNamePresent,
    enterDonorName: enterDonorName,
    ajax: ajax,
    somethingWentWrong: somethingWentWrong,
  };
});
