/*global $, document, Chart*/
$(document).ready(function() {
  "use strict";

  // Main Template Color
  var brandPrimary = "#33b35a";

  // ------------------------------------------------------- //
  // Pie Chart
  // ------------------------------------------------------ //
  var PIECHART = $("#pieChart");
  new Chart(PIECHART, {
    type: "doughnut",
    data: {
      labels: ["Apple", "Others", "Microsoft"],
      datasets: [{
        data: [300, 50, 100],
        borderWidth: [1, 1, 1],
        backgroundColor: [brandPrimary, "rgba(75,192,192,1)", "#FFCE56"],
        hoverBackgroundColor: [brandPrimary, "rgba(75,192,192,1)", "#FFCE56"]
      }]
    }
  });
});
