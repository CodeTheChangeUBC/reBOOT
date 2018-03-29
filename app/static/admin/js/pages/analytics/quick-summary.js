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
      donations: 0,
      item: 0
    },
    average: {
      donationPerDonor: "",
      itemPerDonation: "",
      valuePerDonation: ""
    }
  };

  function getRangedData(model, startDate, endDate, force) {
    var promises = [];

    $.each(quickSummaryData["ranged"], function(key) {
      if (model && model !== key) {
        return;
      }
      promises.push(
        util.totalQuantity(key, startDate, endDate, force).then(function(data) {
          quickSummaryData["ranged"][key] = data;
        })
      );
    });

    return Promise.all(promises).then(function() {
      return quickSummaryData["ranged"];
    });
  }

  function getTotalData(force) {
    return util
      .totalQuantityAll(undefined, undefined, force)
      .then(function(data) {
        quickSummaryData["total"] = data;
        return quickSummaryData["total"];
      });
  }

  return {
    getRangedData: getRangedData,
    getTotalData: getTotalData
  };
});
