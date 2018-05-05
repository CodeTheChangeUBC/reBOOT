"use strict";

define(["../analytics-util", "./analytics-graph"], function(util, Graph) {

  function BarChart(elementId, keyName, valueName, startDate, endDate, color) {
    Graph.call(this, elementId, keyName, valueName, startDate, endDate, color);
  }

  BarChart.prototype = Object.create(Graph.prototype);
  BarChart.prototype.constructor = BarChart;

  BarChart.prototype.updateChart = function(startDate, endDate) {
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
          var BARCHART = $(that._elementID);

          that._chart = new Chart(BARCHART, {
            type: "bar",
            options: {
              legend: {
                display: false
              }
            },
            data: {
              labels: keysAndValues.keys,
              datasets: [{
                label: "Donated items per city",
                backgroundColor: brandPrimary,
                borderWidth: 1,
                hoverBackgroundColor: brandSecondary,
                hoverBoardColor: brandSecondary,
                hoverBoarderWidth: 1,
                data: keysAndValues.values,
              }]
            }
          })
        }
      });
  };

  return BarChart;
});