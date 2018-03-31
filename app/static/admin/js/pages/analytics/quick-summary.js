"use strict";

define(["./analytics-util"], function(util) {
  var quickSummaryData = {
    ranged: {
      donor: 0,
      donation: 0,
      item: 0
    },
    total: {
      donor: 0,
      donation: 0,
      item: 0
    },
    calculated: {
      donationPerDonor: "",
      itemPerDonation: "",
      valuePerDonation: ""
    }
  };

  function getRangedData(model, startDate, endDate, force) {
    var promises = [];

    $.each(quickSummaryData.ranged, function(key) {
      if (model && model !== key) {
        return;
      }
      promises.push(
        util.totalQuantity(key, startDate, endDate, force).then(function(data) {
          quickSummaryData.ranged[key] = _objAcculmulator(data);
        })
      );
    });

    return Promise.all(promises).then(function() {
      return quickSummaryData.ranged;
    });
  }

  function getTotalData(force) {
    return util
      .totalQuantityAll(undefined, undefined, force)
      .then(function(data) {
        quickSummaryData.total = _objAcculmulator(data);
        return quickSummaryData.total;
      });
  }

  function getAverageData(force) {
    // var avera
    // return getTotalData().then(function(total) {
    // })
  }

  function setQuickSummary(domObj) {
    $.each(quickSummaryData, function(type, model) {
      $.each(model, function(key) {
        if (domObj[type].hasOwnProperty(key)) {
          console.log(quickSummaryData[type][key]);
          $(domObj[type][key]).text(quickSummaryData[type][key]);
        }
      });
    });
  }

  function setUp(domObj) {
    return Promise.all([getRangedData(), getTotalData()])
      .then(function() {
        return getAverageData();
      })
      .then(function() {
        return setQuickSummary(domObj);
      });
  }

  function _objAcculmulator(obj, acc = 0) {
    if (typeof obj !== "object") {
      return obj;
    }

    $.each(obj, function(key, value) {
      acc += value;
    });
    return acc;
  }

  return {
    setUp: setUp
  };
});
