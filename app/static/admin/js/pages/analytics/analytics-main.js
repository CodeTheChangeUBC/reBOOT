"use strict";

define(function(require) {
  var quickSummaryDom = {
    ranged: {
      donor: "#newDonors",
      donation: "#newDonations",
      item: "#newItems"
    },
    total: {
      donor: "#totalDonors",
      donation: "#totalDonations",
      item: "#totalItems"
    },
    calculated: {
      donationPerDonor: "#avgDonationPerDonor",
      itemPerDonation: "#avgItemPerDonation",
      valuePerDonation: "#valuePerDonation"
    }
  };

  var quickSummary = require("./quick-summary");
  //   var itemPercentagePieChart = require("./item-percentage");
  //   var itemLocationBarChart = require("./item-location");
  var itemNumberLineChart = require("./item-number");

  var promises = [
    quickSummary.setUp(quickSummaryDom),
    itemNumberLineChart.createChart("#lineChart")
  ];

  Promise.all(promises).then(function() {
    // loadingOff();
  });
});
