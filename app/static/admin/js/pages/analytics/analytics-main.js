"use strict";

define(function (require) {
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
      itemPerDonation: "#avgItemPerDonation"
    }
  };

  var quickSummary = require("./quick-summary");
  //   var itemPercentagePieChart = require("./item-percentage");
  var locationBarChart = require("./item-location");
  var itemNumberLineChart = require("./item-number");

  var promises = [
    quickSummary.setUp(quickSummaryDom),
    itemNumberLineChart.createChart("#lineChart"),
    locationBarChart.createChart("#locationBarChart")
  ];

  Promise.all(promises).then(function () {
    $("body").addClass("loaded");
  });
});
