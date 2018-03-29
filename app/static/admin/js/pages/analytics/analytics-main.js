"use strict";

define(function(require) {
  var quickSummary = require("./quick-summary");
  quickSummary.getRangedData().then(function(data) {
    console.log(data);
  });

  quickSummary.getTotalData().then(function(data) {
    console.log(data);
  });

  //   var itemPercentagePieChart = require("./item-percentage");
  //   var itemLocationBarChart = require("./item-location");
  var itemNumberLineChart = require("./item-number");
  itemNumberLineChart.createChart("#lineChart");
});
