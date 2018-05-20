"use strict";

define(["../analytics-util", "../graph/pie-chart"], function(util, PieChart) {

  function ItemStatusController(elementId, keyName, valueName, startDate, endDate, graphOption) {
    this._elementID = elementId;
    this._keyName = keyName;
    this._valueName = valueName;
    this._startDate = startDate;
    this._endDate = endDate;
    this._graphOption = graphOption;
    this._graph = null;
  }

  ItemStatusController.prototype.createGraph = function() {
    var self = this;
    return self.getKeysAndValues()
      .then(function(data) {
        self._graph = new PieChart(self._elementID, data, self._graphOption);
        self._graph.createPieChart();
        return self._graph;
      });
  };

  ItemStatusController.prototype.updateGraph = function(startDate, endDate) {
    var self = this;
    self._startDate = startDate;
    self._endDate = endDate;
    return self.getKeysAndValues()
      .then(function(data) {
        self._graph.updateGraph(data);
        return self._graph;
      });
  };


  ItemStatusController.prototype.getKeysAndValues = function() {
    var self = this;

    return util.totalStatus(self._startDate, self._endDate, true)
      .then(function(data) {
        var keys = util.getKeys(data, self._keyName);
        var values = util.getValues(data, self._valueName);
        return {
          keys: keys,
          values: values
        };
      });
  };

  return ItemStatusController;

});
