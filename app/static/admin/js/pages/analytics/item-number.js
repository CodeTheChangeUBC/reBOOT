/*global Chart*/
"use strict";

define(["./analytics-util"], function(util) {
  var itemQuantityArray = [];

  var totalNumOfItems = function() {
    if (itemQuantityArray.length === 0) {
      return util.aggregateQuantity("item").then(function(data) {
        itemQuantityArray = data.result;
        return itemQuantityArray;
      });
    }
    return itemQuantityArray;
  };

  var chartLabels = function() {
    var itemLabels = [];
    $.each(itemQuantityArray, function(key) {
      itemLabels.push(key);
    });
    return itemLabels;
  };

  var chartValues = function() {
    var itemQuantity = [];
    $.each(itemQuantityArray, function(key, value) {
      itemQuantity.push(value);
    });
    return itemQuantity;
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
        labels: chartLabels(),
        datasets: [
          {
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
            data: chartValues(),
            spanGaps: false
          }
        ]
      }
    });
  };

  var createChart = function(chartId) {
    return totalNumOfItems().then(function() {
      drawChart(chartId);
    });
  };

  return {
    createChart: createChart
  };
});
