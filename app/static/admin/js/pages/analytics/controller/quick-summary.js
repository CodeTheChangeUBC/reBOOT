"use strict";

define(["../analytics-util", "../constants"], function(util, c) {
  var quickSummaryData = {
    ranged: {
      donor: 0,
      donation: 0,
      item: 0,
      value: 0
    },
    total: {
      donor: 0,
      donation: 0,
      item: 0,
      value: 0
    },
    calculated: {
      donationPerDonor: "0",
      itemPerDonor: "0",
      itemPerDonation: "0",
      valuePerItem: "0",
    }
  };

  function getRangedData(startDate, endDate, force) {
    return _getDataHelper(quickSummaryData.ranged, startDate, endDate, force);
  }

  function getTotalData(force) {
    return _getDataHelper(quickSummaryData.total, undefined, undefined, force);
  }

  function getAverageData() {
    var donor = quickSummaryData.total.donor;
    var donation = quickSummaryData.total.donation;
    var item = quickSummaryData.total.item;
    var value = parseInt(quickSummaryData.total.value.slice(1));
    quickSummaryData.calculated.donationPerDonor = (donation / donor).toFixed(1);
    quickSummaryData.calculated.itemPerDonor = (item / donor).toFixed(1);
    quickSummaryData.calculated.itemPerDonation = (item / donation).toFixed(1);
    quickSummaryData.calculated.valuePerItem = (value / item).toFixed(2);
    return quickSummaryData.calculated;
  }

  function setQuickSummary(domObj) {
    $.each(quickSummaryData, function(type, model) {
      $.each(model, function(key) {
        if (domObj[type].hasOwnProperty(key)) {
          $(domObj[type][key]).text(quickSummaryData[type][key]);
        }
      });
    });
  }

  function setUp(domObj, startDate, endDate, force) {
    return Promise.all([getRangedData(startDate, endDate, force), getTotalData(force)])
      .then(function() {
        return getAverageData();
      })
      .then(function() {
        return setQuickSummary(domObj);
      });
  }

  function _getDataHelper(quickSummaryDataObj, startDate, endDate, force) {
    var promises = [];

    $.each(quickSummaryDataObj, function(key) {
      if (key !== "value") {
        promises.push(
          util.totalQuantity(key, startDate, endDate, force).then(function(data) {
            quickSummaryDataObj[key] = _quantityAcculmulator(data);
          })
        );
      }
    });

    return Promise.all(promises)
      .then(function() {
        return util.totalValue(undefined, startDate, endDate, true);
      })
      .then(function(data) {
        quickSummaryDataObj.value = _valueAccumulator(data);
        return quickSummaryDataObj;
      });
  }

  function _quantityAcculmulator(arr, acc = 0) {
    arr.forEach(function(obj) {
      acc += obj[c.TOTAL_QUANTITY];
    });
    return acc;
  }

  function _valueAccumulator(arr, acc = 0) {
    arr.forEach(function(obj) {
      acc += obj[c.TOTAL_VALUE];
    });
    return "$" + acc.toFixed(2);
  }

  return {
    setUp: setUp
  };
});
