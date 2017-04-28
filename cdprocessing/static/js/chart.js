function updateSeries() {
  series = chart.get("main");
  error = chart.get("main_error");
  if ($("#main-series-option").hasClass("off")) {
    series.hide();
    error.hide();
  } else {
    series.show();
    if (($("#main-error-option").hasClass("off"))) {
      error.hide();
    } else {
      error.show();
    }
  }
}

function makeChart(title, xMin, xMax, mainSeries, mainError) {
  var chart = Highcharts.chart("chart", {
      title: {
        text: title,
      },
      chart: {
        type: "line",
        plotBorderWidth: 1,
        plotBorderColor: "#000000",
        margin: [50, 30, 50, 75],
        zoomType: "xy",
        height: "50%",
        animation: true
      },
      credits: {
        enabled: false
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        arearange: {
          animation: true
        }
      },
      xAxis: {
        min: xMin,
        max: xMax,
        gridLineWidth: 1,
        gridLineColor: "#EEEEEE",
        gridLineDashStyle: "ShortDash",
        lineColor: "#000000",
        tickWidth: 1,
        tickLength: 6,
        tickPosition: "inside",
        tickColor: "#000000",
        title: {
          text: "Wavelength (nm)",
          style: {"font-weight": "bold"}
        }
      },
      yAxis: {
        gridLineWidth: 1,
        gridLineColor: "#EEEEEE",
        gridLineDashStyle: "ShortDash",
        tickWidth: 1,
        tickLength: 6,
        tickPosition: "inside",
        lineColor: "#000000",
        tickColor: "#000000",
        title: {
          text: "Circular Dichroism",
          style: {"font-weight": "bold"}
        }
      },
      tooltip: {
        enabled: false
      },
      series: [{
        data: mainError,
        id: "main_error",
        color: "#4A9586",
        type: "arearange",
        fillOpacity: 0.2,
        lineWidth: 0,
        enableMouseTracking: false
      }, {
        data: mainSeries,
        id: "main",
        color: "#4A9586",
        lineWidth: 1.5,
        marker: {
          enabled: false,
          states: {
            hover: {
              enabled: false
            }
          }
        }
      }]
    });
    return chart;
}


// When the page has finished loading...
$( document ).ready(function() {
  // Scroll to the top of the chart
  $("html, body").animate({
    scrollTop: $("#chart").offset().top
  }, 800);

  // Add an event handler for the main error button
  $("#main-error-option").click(function () {
    if ($("#main-error-option").hasClass("on")) {
      $("#main-error-option").addClass("off").removeClass("on");
    } else {
      $("#main-error-option").addClass("on").removeClass("off");
    }
    updateSeries();
  });

  // Add an event handler for the main series button
  $("#main-series-option").click(function () {
    if ($("#main-series-option").hasClass("on")) {
      $("#main-series-option").addClass("off").removeClass("on");
    } else {
      $("#main-series-option").addClass("on").removeClass("off");
    }
    updateSeries();
  });
});
