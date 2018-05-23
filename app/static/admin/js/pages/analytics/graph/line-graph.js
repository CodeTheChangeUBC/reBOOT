"use strict";

define(["../analytics-util", "./graph"], function(util, Graph) {

  function LineGraph(elementId, data, option) {
    Graph.call(this, elementId, data, option);
  }

  LineGraph.prototype = Object.create(Graph.prototype);
  LineGraph.prototype.constructor = LineGraph;

  LineGraph.prototype.createLineGraph = function() {
    var self = this;

    var brandPrimary = self._option.color.primary;
    var brandSecondary = self._option.color.secondary;
    var LINECHART = $(self._elementID);

    self._chart = new Chart(LINECHART, {
      type: "line",
      options: {
        legend: {
          display: false
        }
      },
      data: {
        labels: self._data.keys,
        datasets: [{
          label: self._option.label,
          fill: true,
          lineTension: 0.3,
          backgroundColor: brandPrimary,
          borderColor: brandPrimary,
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0.0,
          borderJoinStyle: "miter",
          borderWidth: 1,
          pointBorderColor: brandPrimary,
          pointBackgroundColor: "#fff",
          pointBorderWidth: 1,
          pointHoverRadius: 4,
          pointHoverBackgroundColor: brandSecondary,
          pointHoverBorderColor: brandSecondary,
          pointHoverBorderWidth: 1,
          pointRadius: 4,
          pointHitRadius: 0,
          data: self._data.values,
          spanGaps: false
        }]
      }
    });
  };

  return LineGraph;
});
