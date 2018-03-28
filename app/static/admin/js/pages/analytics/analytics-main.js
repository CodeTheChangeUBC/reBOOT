"use strict";

define(function(require) {
  var quickSummary = require("./quick-summary");

  //   var itemPercentagePieChart = require("./item-percentage");
  //   var itemLocationBarChart = require("./item-location");
  var itemNumberLineChart = require("./item-number");
  itemNumberLineChart.createChart("#lineChart");
});
