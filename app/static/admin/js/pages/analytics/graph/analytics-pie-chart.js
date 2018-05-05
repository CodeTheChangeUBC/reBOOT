"use strict";

define(["../analytics-util", "./analytics-graph"], function(util, Graph) {

  function PieChart(elementId, keyName, valueName, startDate, endDate) {
    Graph.call(this, elementId, keyName, valueName, startDate, endDate, null);
  }

  PieChart.prototype = Object.create(Graph.prototype);
  PieChart.prototype.constructor = PieChart;

  PieChart.prototype.updateChart = function(startDate, endDate) {
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
          var CHART = $(that._elementID);

          that._chart = new Chart(CHART, {
            type: 'doughnut',
            data: {
              labels: keysAndValues.keys,
              datasets: [{
                data: keysAndValues.values,
                borderWidth: [1, 1, 1],
                backgroundColor: [
                  "rgba(41, 137, 233, 0.3)",
                  "rgba(227, 48, 17, 0.3)",
                  "rgba(75,192,192,1)",
                ],
                hoverBackgroundColor: [
                  "#448AFF",
                  "#E33011",
                  "rgba(75,192,192,1)",
                ]
              }]
            }
          });
        }
      })
  };

  return PieChart;
});



//
// /*
// Private
//  */
//
// function _seperateValuesKeyAndValue(startDate, endDate, force) {
//   if (
//     itemValueKeys.length === 0 ||
//     itemValueValues.length === 0 ||
//     force
//   ) {
//     return util
//       .totalValue("item", startDate, endDate, true)
//       .then(function(data) {
//         itemValueKeys = _getDates(data);
//         itemValueValues = _getValues(data);
//         return data;
//       });
//   }
// }