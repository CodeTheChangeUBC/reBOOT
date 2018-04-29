/*global Chart*/
"use strict";

define(["./analytics-util"], function(util) {
  var itemStatusKeys = [];
  var itemStatusValues = [];

  function totalStatusofItems(startDate, endDate, force) {
    if (
      itemStatusKeys.length === 0 ||
      itemStatusValues.length === 0 ||
      force
    ) {
      return util
        .totalStatus(startDate, endDate, true)
        .then(function(data) {
          itemStatusKeys = getStatuses(data);
          itemStatusValues = getQuantities(data);
          return data;
        });
    }
  }

  function drawChart(elementId) {
    // Main Template Color
    var brandPrimary = "#33b35a";
    var CHART = $(elementId);

    new Chart(CHART, {
      type: 'doughnut',
      data: {
        labels: itemStatusKeys,
        datasets: [{
          data: itemStatusValues,
          borderWidth: [1, 1, 1],
          backgroundColor: [
            brandPrimary,
            "rgba(75,192,192,1)",
            "#FFCE56"
          ],
          hoverBackgroundColor: [
            brandPrimary,
            "rgba(75,192,192,1)",
            "#FFCE56"
          ]
        }]
      }
    });
  }

  function createChart(chartId, startDate, endDate, force) {
    return totalStatusofItems(startDate, endDate, force).then(function() {
      drawChart(chartId);
    });
  }

  function getQuantities(arr) {
    var quantities = [];
    arr.forEach(function(obj) {
      quantities.push(obj.count);
    });
    return quantities;
  }

  function getStatuses(arr) {
    var statuses = [];
    arr.forEach(function(obj) {
      statuses.push(util.toTitleCase(obj.status));
    });
    return statuses;
  }

  return {
    createChart: createChart
  };
});
