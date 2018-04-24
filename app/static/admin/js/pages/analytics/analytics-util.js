"use strict";

define(function() {
  var totalQuantityObj = {
    donor: [],
    donation: [],
    item: []
  };
  var totalValueObj = {
    donor: [],
    donation: [],
    item: []
  };

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

  var aggregateStatus = function(startDate, endDate) {
    return $.ajax({
      beforeSend: csrf,
      url: "/api/status",
      type: "GET",
      dataType: "json",
      data: {
        startDate: startDate,
        endDate: endDate
      }
    });
  };

  var totalStatus = function(startDate, endDate, force) {
    if (force) {
      return aggregateStatus(startDate, endDate).then(function(data) {
        return data.result;
      });
    }
  };

  var totalQuantity = function(model, startDate, endDate, force) {
    if (force || totalQuantityObj[model].length === 0) {
      return aggregateQuantity(model, startDate, endDate).then(function(data) {
        totalQuantityObj[model] = data.result;
        return totalQuantityObj[model];
      });
    }
    return new Promise(function(resolve) {
      resolve(totalQuantityObj[model]);
    });
  };

  var totalQuantityAll = function(startDate, endDate, force) {
    var promises = [];
    $.each(totalQuantityObj, function(key) {
      promises.push(
        new Promise(function(resolve) {
          totalQuantity(key, startDate, endDate, force).then(function(data) {
            resolve(data);
          });
        })
      );
    });
    return Promise.all(promises).then(function() {
      return totalQuantityObj;
    });
  };

  var totalValue = function(model, startDate, endDate, force) {
    if (force || totalValueObj[model].length === 0) {
      return aggregateValue(model, startDate, endDate).then(function(data) {
        totalValueObj[model] = data.result;
        return totalValueObj[model];
      });
    }
    return new Promise(function(resolve) {
      resolve(totalValueObj[model]);
    });
  };

  var totalValueAll = function(startDate, endDate, force) {
    var promises = [];
    $.each(totalValueObj, function(key) {
      promises.push(
        new Promise(function(resolve) {
          totalValue(key, startDate, endDate, force).then(function(data) {
            resolve(data);
          });
        })
      );
    });
    return Promise.all(promises).then(function() {
      return totalValueObj;
    });
  };

  function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
  }

  return {
    totalValue: totalValue,
    totalValueAll: totalValueAll,
    totalQuantity: totalQuantity,
    totalQuantityAll: totalQuantityAll,
    totalStatus: totalStatus,
    toTitleCase: toTitleCase
  };
});
