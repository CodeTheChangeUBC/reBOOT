/*global Chart*/
"use strict";

define(["./analytics-util"], function(util) {
    var itemValueKeys = [];
    var itemValueValues = [];

    function createChart(chartId, startDate, endDate, force) {
        return _seperateValuesKeyAndValue(startDate, endDate, force).then(function() {
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
            type: "line",
            options: {
                legend: {
                    display: false
                }
            },
            data: {
                labels: itemValueKeys,
                datasets: [
                    {
                        label: "Donations per day",
                        fill: true,
                        lineTension: 0.3,
                        backgroundColor: "rgba(77, 193, 75, 0.4)",
                        borderColor: brandPrimary,
                        borderCapStyle: "butt",
                        borderDash: [],
                        borderDashOffset: 0.0,
                        borderJoinStyle: "miter",
                        borderWidth: 1,
                        pointBorderColor: brandPrimary,
                        pointBackgroundColor: "#fff",
                        pointBorderWidth: 1,
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: brandPrimary,
                        pointHoverBorderColor: "rgba(220,220,220,1)",
                        pointHoverBorderWidth: 2,
                        pointRadius: 5,
                        pointHitRadius: 0,
                        data: itemValueValues,
                        spanGaps: false
                    }
                ]
            }
        });
    }

    function _seperateValuesKeyAndValue(startDate, endDate, force) {
        if (
            itemValueKeys.length === 0 ||
            itemValueValues.length === 0 ||
            force
        ) {
            return util
                .totalValue("item", startDate, endDate, true)
                .then(function(data) {
                    itemValueKeys = _getDates(data);
                    itemValueValues = _getValues(data);
                    return data;
                });
        }
    }

    function _getValues(arr) {
        var quantities = [];
        arr.forEach(function(obj) {
            quantities.push(obj["total_value"]);
        });
        return quantities;
    }

    function _getDates(arr) {
        var dates = [];
        arr.forEach(function(obj) {
            dates.push(obj["created_at_formatted"]);
        });
        return dates;
    }

    return {
        createChart: createChart
    };
});
