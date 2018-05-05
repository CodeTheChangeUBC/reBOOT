"use strict";

define(["../analytics-util", "../constants"], function(util, c) {

  function Graph(elementId, keyName, valueName, startDate, endDate, color) {
    this._elementID = elementId;
    this._keyName = keyName;
    this._valueName = valueName;
    this._startDate = startDate;
    this._endDate = endDate;
    this._color = color;
    this._chart = undefined;
  }

  Graph.prototype.getKeysAndValues = function() {
    var that = this;

    return _getAppropriateData().then(function (data) {
      var keys = _getKeys(data);
      var values = _getValues(data);
      return {keys: keys, values: values}
    });

    /*
    Private Functions
     */

    function _getAppropriateData() {
      if (that._keyName === c.CREATED_AT_FORMATTED) {
        if (that._valueName === c.TOTAL_QUANTITY) {
          return util.totalQuantity(c.ITEM, that._startDate, that._endDate, true);
        }
        else {
          return util.totalValue(c.ITEM, that._startDate, that._endDate, true);
        } // value(y-axis) = value
      } else if (that._keyName === c.LOCATION) {
        return util.totalLocation(that._startDate, that._endDate);
      } else {
        return util.totalStatus(that._startDate, that._endDate, true);
      }
    }

    function _getKeys(arr) {
      var keys = [];
      arr.forEach(function(obj) {
        var key = obj[that._keyName];
        if (key) {
          keys.push(key);
        } else {
          keys.push("Unknown");
        }
      });
      return keys;
    }

    function _getValues(arr) {
      var values = [];
      arr.forEach(function(obj) {
        values.push(obj[that._valueName]);
      });
      return values;
    }
  };

  return Graph;
});