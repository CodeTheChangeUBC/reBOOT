/*global moment*/
"use strict";

define(function(require) {
  var quickSummary = require("./quick-summary");
  var itemStatusPieChart = require("./item-status");
  var locationBarChart = require("./item-location");
  var itemNumberLineChart = require("./item-number");
  var dateValueLineChart = require("./date-value");

  var quickSummaryDom = {
    ranged: {
      donor: "#rangedDonors",
      donation: "#rangedDonations",
      item: "#rangedItems",
      value: "#rangedValues"
    },
    total: {
      donor: "#totalDonors",
      donation: "#totalDonations",
      item: "#totalItems",
      value: "#totalValues"
    },
    calculated: {
      donationPerDonor: "#avgDonationPerDonor",
      temPerDonor: "#avgItemPerDonor",
      itemPerDonation: "#avgItemPerDonation",
      valuePerItem: "#avgValuePerItem",
    }
  };

  // dateRangePicker initialization
  var start = moment().subtract(2, 'years');
  var end = moment().subtract(1, 'years');

  function cb(start, end) {
      $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));

      var startDate = start.format('YYYY-MM-DD');
      var endDate = end.format('YYYY-MM-DD');

      var promises = [
          quickSummary.setUp(quickSummaryDom, startDate, endDate, true),
          itemNumberLineChart.createChart("#itemNumberLineChart", startDate, endDate, true),
          itemStatusPieChart.createChart("#pieChart", startDate, endDate, true),
          locationBarChart.createChart("#locationBarChart", startDate, endDate, true),
          dateValueLineChart.createChart("#dateValueLineChart", startDate, endDate, true)
      ];

      return Promise.all(promises);
  }
  $('#reportrange').daterangepicker({
      startDate: start,
      endDate: end,
      ranges: {
          'Today': [moment(), moment()],
          'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
          'Last 7 Days': [moment().subtract(6, 'days'), moment()],
          'Last 30 Days': [moment().subtract(29, 'days'), moment()],
          'This Month': [moment().startOf('month'), moment().endOf('month')],
          'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
          'This Year': [moment().startOf('year'), moment().endOf('year')],
          'Last Year': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')],
          'Total': [moment().subtract(30, 'year').startOf('year'), moment().endOf('year')]
      }
  }, cb);

  cb(start, end)
      .then(function() {
          $("body").addClass("loaded");
      })
      .catch(function(err) {
          console.log(err);
      })
});
