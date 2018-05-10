/*global Chart*/
"use strict";

define(["../analytics-util", "./graph"], function(util, Graph) {

  function BarChart(elementId, data, option) {
    Graph.call(this, elementId, data, option);
  }

  BarChart.prototype = Object.create(Graph.prototype);
  BarChart.prototype.constructor = BarChart;

  BarChart.prototype.createBarChart = function() {
    var self = this;

    var brandPrimary = self._option.color.primary;
    var brandSecondary = self._option.color.secondary;
    var BARCHART = $(self._elementID);

    self._chart = new Chart(BARCHART, {
      type: "bar",
      options: {
        legend: {
          display: false
        }
      },
      data: {
        labels: util.arrayToTitleCase(self._data.keys),
        datasets: [{
          label: self._option.label,
          backgroundColor: brandPrimary,
          borderWidth: 1,
          hoverBackgroundColor: brandSecondary,
          hoverBoardColor: brandSecondary,
          hoverBoarderWidth: 1,
          data: self._data.values,
        }]
      }
    });
  };

  return BarChart;
});
