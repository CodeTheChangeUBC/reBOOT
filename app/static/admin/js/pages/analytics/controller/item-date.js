"use strict";

define(["../analytics-util", "../graph/line-graph", "../constants"], function(util, LineGraph, c) {

  function ItemDateController(elementId, keyName, valueName, startDate, endDate, graphOption) {
    this._elementID = elementId;
    this._keyName = keyName;
    this._valueName = valueName;
    this._startDate = startDate;
    this._endDate = endDate;
    this._graphOption = graphOption;
    this._graph = null;
  }

  ItemDateController.prototype.createGraph = function() {
    var self = this;
    return self.getKeysAndValues()
      .then(function(data) {
        self._graph = new LineGraph(self._elementID, data, self._graphOption);
        self._graph.createLineGraph();
        return self._graph;
      });
  };

  ItemDateController.prototype.updateGraph = function(startDate, endDate) {
    var self = this;
    self._startDate = startDate;
    self._endDate = endDate;
    return self.getKeysAndValues()
      .then(function(data) {
        self._graph.updateGraph(data);
        return self._graph;
      });
  };


  ItemDateController.prototype.getKeysAndValues = function() {
    var self = this;

    return util.totalQuantity(c.ITEM, self._startDate, self._endDate, true)
      .then(function (data) {
        var keys = util.getKeys(data, self._keyName);
        var values = util.getValues(data, self._valueName);
        return {keys: keys, values: values}
    });
  };

  return ItemDateController;
});