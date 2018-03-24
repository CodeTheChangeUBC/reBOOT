"use strict";

define(function(require) {
  var quickSummary = require("./quick-summary");

  quickSummary.consoleLog("hello");
  console.log(quickSummary.totalNumOfItems());
  console.log(quickSummary.totalValueOfItems());

  // quickSummary.totalNumOfItems().then(function(data) )
  //   var itemPercentagePieChart = require("./item-percentage");
  //   var itemLocationBarChart = require("./item-location");
  //   var itemNumberLineChart = require("./item-number");
});
