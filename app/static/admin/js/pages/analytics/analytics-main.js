/*global moment*/
"use strict";

define(function(require) {
  var quickSummary = require("./quick-summary");
  var LineGraph = require("./graph/analytics-line-graph");
  var BarChart = require("./graph/analytics-bar-chart");
  var PieChart = require("./graph/analytics-pie-chart");
  var c = require("./constants");

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
  var start = moment().subtract(1, 'years');
  var end = moment();

  var itemStatusPieChart = new PieChart("#pieChart", c.STATUS, c.COUNT, start, end);
  var locationBarChart = new BarChart("#locationBarChart", c.LOCATION, c.COUNT, start, end, {p: "#FFD180", s: "#FFAB40"});
  var itemNumberLineChart = new LineGraph("#itemNumberLineChart", c.CREATED_AT_FORMATTED, c.TOTAL_QUANTITY, start, end, {p: "rgba(77, 193, 75, 0.4)", s: "#33b35a"});
  var dateValueLineChart = new LineGraph("#dateValueLineChart", c.CREATED_AT_FORMATTED, c.TOTAL_VALUE, start, end, {p: "rgba(227, 48, 17, 0.3)", s: "#ff5252"});

  function cb(start, end) {
    $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));

    var startDate = start.format('YYYY-MM-DD');
    var endDate = end.format('YYYY-MM-DD');

    var promises = [
      quickSummary.setUp(quickSummaryDom, startDate, endDate, true),
      itemNumberLineChart.updateChart(startDate, endDate),
      itemStatusPieChart.updateChart(startDate, endDate),
      locationBarChart.updateChart(startDate, endDate),
      dateValueLineChart.updateChart(startDate, endDate)
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
