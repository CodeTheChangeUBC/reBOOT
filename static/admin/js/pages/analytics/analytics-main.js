/*global moment*/
"use strict";

define(function(require) {
    var quickSummary = require("./controller/quick-summary");
    var ItemDateController = require("./controller/item-date");
    var ItemLocationController = require("./controller/item-location");
    var ItemStatusController = require("./controller/item-status");
    var ValueDateController = require("./controller/value-date");
    var c = require("./constants");

    var quickSummaryDom = {
        ranged: {
            donor: "#rangedDonors",
            donation: "#rangedDonations",
            item: "#rangedItems",
            value: "#rangedValues"
        },
        total: {
            donor: "#totalDonors",
            donation: "#totalDonations",
            item: "#totalItems",
            value: "#totalValues"
        },
        calculated: {
            donationPerDonor: "#avgDonationPerDonor",
            itemPerDonor: "#avgItemPerDonor",
            itemPerDonation: "#avgItemPerDonation",
            valuePerItem: "#avgValuePerItem",
        }
    };

    // dateRangePicker initialization
    var startMoment = moment().subtract(1, 'years');
    var endMoment = moment();
    var start = startMoment.format('YYYY-MM-DD');
    var end = endMoment.format('YYYY-MM-DD');

    var itemDateGraphOption = {
        color: {
            primary: "rgba(77, 193, 75, 0.4)",
            secondary: "#33b35a"
        },
        label: "Donated item per date"
    };
    var itemLocationGraphOption = {
        color: {
            primary: "#FFD180",
            secondary: "#FFAB40"
        },
        label: "Donated item per city"
    };
    var itemStatusGraphOption = {
        color: {
            primary: "rgba(41, 137, 233, 0.3)",
            secondary: "#448AFF"
        },
        label: "# of Item status"
    };
    var valueDateGraphOption = {
        color: {
            primary: "rgba(227, 48, 17, 0.3)",
            secondary: "#ff5252"
        },
        label: "Donated item per date"
    };

    var itemDateController = new ItemDateController("#itemNumberLineChart", c.DOCUMENTED_AT, c.TOTAL_QUANTITY, start, end, itemDateGraphOption);
    var itemLocationController = new ItemLocationController("#locationBarChart", c.LOCATION, c.COUNT, start, end, itemLocationGraphOption);
    var itemStatusController = new ItemStatusController("#itemStatusPieChart", c.STATUS, c.COUNT, start, end, itemStatusGraphOption);
    var valueDateController = new ValueDateController("#dateValueLineChart", c.DOCUMENTED_AT, c.TOTAL_VALUE, start, end, valueDateGraphOption);

    function initializeAnalyticsTools(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));

        var startDate = start.format('YYYY-MM-DD');
        var endDate = end.format('YYYY-MM-DD');

        var initializationPromises = [
            quickSummary.setUp(quickSummaryDom, startDate, endDate, true),
            itemDateController.createGraph(),
            itemLocationController.createGraph(),
            itemStatusController.createGraph(),
            valueDateController.createGraph()
        ];

        return Promise.all(initializationPromises);
    }

    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));

        var startDate = start.format('YYYY-MM-DD');
        var endDate = end.format('YYYY-MM-DD');

        var promises = [
            quickSummary.setUp(quickSummaryDom, startDate, endDate, true),
            itemDateController.updateGraph(startDate, endDate),
            itemLocationController.updateGraph(startDate, endDate),
            itemStatusController.updateGraph(startDate, endDate),
            valueDateController.updateGraph(startDate, endDate)
        ];

        return Promise.all(promises);
    }

    $('#reportrange').daterangepicker({
        startDate: startMoment,
        endDate: endMoment,
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
            'This Year': [moment().startOf('year'), moment().endOf('year')],
            'Last Year': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')],
            'Fiscal Year': [moment().subtract(getAprilOffest(moment().month()), 'month').startOf('month'), moment()],
            'Total': [moment().subtract(50, 'year').startOf('year'), moment().endOf('year')]
        }
    }, cb);

    initializeAnalyticsTools(startMoment, endMoment)
        .then(function() {
            $("body").addClass("loaded");
        })
        .catch(function(err) {
            console.error(err);
        });
    
    // month in moment is 0 based index
    function getAprilOffest(currMonth) {
        let offset = currMonth-3;
        offset = offset<0 ? offset+12 : offset;
        return offset;
    }
});
