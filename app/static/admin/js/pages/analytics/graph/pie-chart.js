"use strict";

define(["../analytics-util", "./graph"], function(util, Graph) {

  function PieChart(elementId, data, option) {
    Graph.call(this, elementId, data, option);
  }

  PieChart.prototype = Object.create(Graph.prototype);
  PieChart.prototype.constructor = PieChart;

  PieChart.prototype.createPieChart = function() {
    var self = this;

    var brandPrimary = self._option.color.primary;
    var brandSecondary = self._option.color.secondary;
    var CHART = $(self._elementID);

    self._chart = new Chart(CHART, {
      type: 'doughnut',
      data: {
        labels: self._data.keys,
        datasets: [{
          data: self._data.values,
          borderWidth: [1, 1, 1],
          backgroundColor: [
            brandPrimary,
            "rgba(227, 48, 17, 0.3)",
            "rgba(75,192,192,1)",
          ],
          hoverBackgroundColor: [
            brandSecondary,
            "#E33011",
            "rgba(75,192,192,1)",
          ]
        }]
      }
    });
  };

  return PieChart;
});