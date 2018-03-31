/*global Chart*/
"use strict";

define(["./analytics-util"], function(util) {
  var itemQuantityKeys = [];
  var itemQuantityValues = [];

  var totalNumOfItems = function(startDate, endDate, force) {
    if (
      itemQuantityKeys.length === 0 ||
      itemQuantityValues.length === 0 ||
      force
    ) {
      return util
        .totalQuantity("item", startDate, endDate, true)
        .then(function(data) {
          itemQuantityKeys = Object.keys(data);
          itemQuantityValues = Object.values(data);
          return data;
        });
    }
  };

  var drawChart = function(elementId) {
    // Main Template Color
    var brandPrimary = "#33b35a";
    var LINECHART = $(elementId);
    new Chart(LINECHART, {
      type: "line",
      options: {
        legend: {
          display: false
        }
      },
      data: {
        labels: itemQuantityKeys,
        datasets: [{
          label: "My First dataset",
          fill: true,
          lineTension: 0.3,
          backgroundColor: "rgba(77, 193, 75, 0.4)",
          borderColor: brandPrimary,
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0.0,
          borderJoinStyle: "miter",
          borderWidth: 1,
          pointBorderColor: brandPrimary,
          pointBackgroundColor: "#fff",
          pointBorderWidth: 1,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: brandPrimary,
          pointHoverBorderColor: "rgba(220,220,220,1)",
          pointHoverBorderWidth: 2,
          pointRadius: 5,
          pointHitRadius: 0,
          data: itemQuantityValues,
          spanGaps: false
        }]
      }
    });
  };

  var createChart = function(chartId, startDate, endDate, force) {
    return totalNumOfItems(startDate, endDate, force).then(function() {
      drawChart(chartId);
    });
  };

  return {
    createChart: createChart
  };
});
