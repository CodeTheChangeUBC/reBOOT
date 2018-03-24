"use strict";

define(["./analytics-util"], function(util) {
  var consoleLog = function(field) {
    console.log(field);
  };

  var totalNumOfItems = function() {
    return util.aggregateQuantity("item");
  };

  var totalValueOfItems = function() {
    return util.aggregateValue("item");
  };

  return {
    consoleLog: consoleLog,
    totalNumOfItems: totalNumOfItems,
    totalValueOfItems: totalValueOfItems
  };
});
