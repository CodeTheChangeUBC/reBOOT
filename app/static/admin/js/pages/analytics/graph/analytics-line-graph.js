"use strict";

define(["../analytics-util", "./analytics-graph"], function(util, Graph) {

  function LineGraph(elementId, keyName, valueName, startDate, endDate, color) {
    Graph.call(this, elementId, keyName, valueName, startDate, endDate, color);
  }

  LineGraph.prototype = Object.create(Graph.prototype);
  LineGraph.prototype.constructor = LineGraph;

  LineGraph.prototype.updateChart = function(startDate, endDate) {
    var that = this;
    that._startDate = startDate;
    that._endDate = endDate;

    Graph.prototype.getKeysAndValues.call(this)
      .then(function (keysAndValues) {
        if (that._chart !== undefined) {
          that._chart.data.labels = keysAndValues.keys;
          that._chart.data.datasets[0].data = keysAndValues.values;
          that._chart.update();
        } else {
          var brandPrimary = that._color.p;
          var brandSecondary = that._color.s;
          var LINECHART = $(that._elementID);

          that._chart = new Chart(LINECHART, {
            type: "line",
            options: {
              legend: {
                display: false
              }
            },
            data: {
              labels: keysAndValues.keys,
              datasets: [
                {
                  label: "Donations per day",
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
                  data: keysAndValues.values,
                  spanGaps: false
                }
              ]
            }
          });
        }
      });
  };
  return LineGraph;
});