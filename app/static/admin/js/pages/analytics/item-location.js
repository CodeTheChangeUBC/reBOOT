/*global Chart*/
"use strict";

define(["./analytics-util"], function (util) {
  var itemLocationKeys = [];
  var itemLocationValues = [];

  function createChart(chartId, startDate, endDate, force) {
    return _seperateLocationKeysAndValues(startDate, endDate, force).then(function () {
      _drawChart(chartId);
    });
  }

  /*
  Private
  */

  function _drawChart(elementId) {
    // Main Template Color
    var brandPrimary = "#33b35a";
    var LINECHART = $(elementId);
    new Chart(LINECHART, {
      type: "bar",
      options: {
        legend: {
          display: false
        }
      },
      data: {
        labels: itemLocationKeys,
        datasets: [
          {
            label: "Donations per day",
            backgroundColor: "rgba(77, 193, 75, 0.4)",
            borderColor: brandPrimary,
            borderWidth: 1,
            hoverBackgroundColor: brandPrimary,
            hoverBoardColor: brandPrimary,
            hoverBoarderWidth: 1,
            data: itemLocationValues,
          }
        ]
      }
    });
  }

  function _seperateLocationKeysAndValues(startDate, endDate, force) {
    if (
      itemLocationKeys.length == 0 ||
      itemLocationValues.length == 0 ||
      force
    ) {
      return util.
        totalProvince(startDate, endDate)
        .then(function (data) {
          itemLocationKeys = _getLocationKeys(data);
          itemLocationValues = _getLocationValues(data);
          return data;
        })
    }
  }

  function _getLocationKeys(arr) {
    var provinces = [];
    arr.forEach(function (obj) {
      provinces.push(obj["location"]);
    });
    return provinces;
  }

  function _getLocationValues(arr) {
    var counts = [];
    arr.forEach(function (obj) {
      counts.push(obj["count"]);
    });
    return counts;
  }

  return {
    createChart: createChart
  };
});