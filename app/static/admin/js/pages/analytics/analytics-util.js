"use strict";

define(function() {
  var cookie = (function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = $.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  })("csrftoken");

  var csrf = function(xhr, settings) {
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", cookie);
    }
  };

  var aggregateQuantity = function(model, startDate, endDate) {
    return $.ajax({
      beforeSend: csrf,
      url: "/api/quantity",
      type: "GET",
      dataType: "json",
      data: {
        model: model,
        startDate: startDate,
        endDate: endDate
      }
    });
  };

  var aggregateValue = function(model, startDate, endDate) {
    return $.ajax({
      beforeSend: csrf,
      url: "/api/value",
      type: "GET",
      dataType: "json",
      data: {
        model: model,
        startDate: startDate,
        endDate: endDate
      }
    });
  };

  return {
    aggregateQuantity: aggregateQuantity,
    aggregateValue: aggregateValue
  };
});
