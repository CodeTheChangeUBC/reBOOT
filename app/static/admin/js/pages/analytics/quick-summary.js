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
      donationPerDonor: "0",
      itemPerDonation: "0",
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
          quickSummaryData.ranged[key] = _objArrAcculmulator(data);
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
        quickSummaryData.total = _totalObjAcculmulator(data);
        return quickSummaryData.total;
      });
  }

  function getAverageData() {
    var donor = quickSummaryData.total.donor;
    var donation = quickSummaryData.total.donation;
    var item = quickSummaryData.total.item;
    quickSummaryData.calculated.donationPerDonor = (donation/donor).toFixed(1);
    quickSummaryData.calculated.itemPerDonation = (item/donation).toFixed(1);
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

  function setUp(domObj) {
    return Promise.all([getRangedData(), getTotalData()])
      .then(function() {
        return getAverageData();
      })
      .then(function() {
        return setQuickSummary(domObj);
      });
  }

  function _objArrAcculmulator(arr, acc = 0) {
    arr.forEach(function(obj) {
      acc += obj.total_quantity;
    });
    return acc;
  }

  function _totalObjAcculmulator(obj) {
    $.each(obj, function(key, value) {
      obj[key] = _objArrAcculmulator(value);
    });
    return obj;
  }

  return {
    setUp: setUp
  };
});
