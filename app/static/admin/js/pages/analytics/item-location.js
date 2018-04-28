/*global Chart*/
"use strict";

define(["./analytics-util"], function(util) {
  var itemLocationKeys = [];
  var itemLocationValues = [];

  function createChart(chartId, startDate, endDate, force) {
    return _separateLocationKeysAndValues(startDate, endDate, force).then(function() {
      _drawChart(chartId);
    });
  }

  /*
  Private
  */

  function _drawChart(elementId) {
    // Main Template Color
    var brandPrimary = "#33b35a";
    var BARCHART = $(elementId);
    new Chart(BARCHART, {
      type: "bar",
      options: {
        legend: {
          display: false
        }
      },
      data: {
        labels: itemLocationKeys,
        datasets: [{
          label: "Donated items per city",
          backgroundColor: "rgba(77, 193, 75, 0.4)",
          borderColor: brandPrimary,
          borderWidth: 1,
          hoverBackgroundColor: brandPrimary,
          hoverBoardColor: brandPrimary,
          hoverBoarderWidth: 1,
          data: itemLocationValues,
        }]
      }
    });
  }

  function _separateLocationKeysAndValues(startDate, endDate, force) {
    if (
      itemLocationKeys.length === 0 ||
      itemLocationValues.length === 0 ||
      force
    ) {
      return util.
      totalProvince(startDate, endDate)
        .then(function(data) {
          itemLocationKeys = _getLocationKeys(data);
          itemLocationValues = _getLocationValues(data);
          return data;
        });
    }
  }

  function _getLocationKeys(arr) {
    var provinces = [];
    arr.forEach(function(obj) {
      if (obj.location === "") {
        provinces.push("Unknown");
      } else {
        provinces.push(obj.location);
      }
    });
    return provinces;
  }

  function _getLocationValues(arr) {
    var counts = [];
    arr.forEach(function(obj) {
      counts.push(obj.count);
    });
    return counts;
  }

  return {
    createChart: createChart
  };
});
