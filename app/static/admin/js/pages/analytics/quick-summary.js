"use strict";

define(["./analytics-util"], function(util) {
  var totalQuantityObj = {
    // donor: [],
    // donation: [],
    item: []
  };
  var totalValueObj = {
    // donor: [],
    // donation: [],
    item: []
  };
  var donorValues;
  var donorQuantity;
  var donationValues;
  var donationQuantity;
  var itemValues;
  var itemQuantity;

  var totalQuantity = function(model, startDate, endDate, force) {
    if (force || totalQuantityObj[model].length === 0) {
      return util
        .aggregateQuantity(model, startDate, endDate)
        .then(function(data) {
          totalQuantityObj[model] = data.result;
          return totalQuantityObj[model];
        });
    }
    return totalQuantityObj[model];
  };

  var totalQuantityAll = function(startDate, endDate, force) {
    var promises = [];
    $.each(totalQuantityObj, function(key, value) {
      promises.push(
        new Promise(function(resolve, reject) {
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
      return util
        .aggregateValue(model, startDate, endDate)
        .then(function(data) {
          totalValueObj[model] = data.result;
          return totalValueObj[model];
        });
    }
    return totalValueObj[model];
  };

  var totalValueAll = function(startDate, endDate, force) {
    var promises = [];
    $.each(totalValueObj, function(key, value) {
      promises.push(
        new Promise(function(resolve, reject) {
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

  totalQuantityAll().then(function(data) {
    console.log(data);
  });

  totalValueAll().then(function(data) {
    console.log(data);
  });

  return {};
});
