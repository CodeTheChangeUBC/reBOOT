"use strict";

define(["./analytics-util"], function(util) {
  util.totalQuantity("item").then(function(data) {
    console.log(data);
  });

  util.totalValue("item").then(function(data) {
    console.log(data);
  });

  return {};
});
