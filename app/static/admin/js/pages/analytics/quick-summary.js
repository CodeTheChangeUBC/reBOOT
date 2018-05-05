"use strict";

define(["./analytics-util"], function(util) {
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

  function getRangedData(kind, startDate, endDate, force) {
    var curQuickSummaryData;
    if (kind === "ranged") {
      curQuickSummaryData = quickSummaryData.ranged;
    } else if (kind === "total") {
      curQuickSummaryData = quickSummaryData.total;
    }
    var promises = [];

    $.each(curQuickSummaryData, function(key) {
      if (key !== "value"){
        promises.push(
          util.totalQuantity(key, startDate, endDate, force).then(function(data) {
            curQuickSummaryData[key] = _quantityAcculmulator(data);
          })
        );
      }
    });

    return Promise.all(promises)
      .then(function() {
        return util.totalValue(undefined, startDate, endDate, true);
      })
      .then(function(data) {
        curQuickSummaryData["value"] = _valueAccumulator(data);
        return curQuickSummaryData;
      });
  }

  function getAverageData() {
    var donor = quickSummaryData.total.donor;
    var donation = quickSummaryData.total.donation;
    var item = quickSummaryData.total.item;
    var value = parseInt(quickSummaryData.total.value.slice(1));
    quickSummaryData.calculated.donationPerDonor = (donation/donor).toFixed(1);
    quickSummaryData.calculated.itemPerDonor = (item/donor).toFixed(1);
    quickSummaryData.calculated.itemPerDonation = (item/donation).toFixed(1);
    quickSummaryData.calculated.valuePerItem = (value/item).toFixed(2);
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
    return Promise.all([getRangedData("ranged", startDate, endDate, force), getRangedData("total", undefined, undefined, force)])
      .then(function() {
        return getAverageData();
      })
      .then(function() {
        return setQuickSummary(domObj);
      });
  }

  function _quantityAcculmulator(arr, acc = 0) {
    arr.forEach(function(obj) {
      acc += obj.total_quantity;
    });
    return acc;
  }

  function _valueAccumulator(arr, acc = 0) {
    arr.forEach(function(obj) {
      acc += obj.total_value;
    });
    return "$" + acc.toFixed(2).toString();
  }

  return {
    setUp: setUp
  };
});
