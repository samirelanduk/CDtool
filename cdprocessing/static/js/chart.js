var COLORS = [
  "#c0392b", "#2980b9", "#f1c40f", "#2c3e50"
]

function updateSeries() {
  $(".series-config").each(function() {
    var series = chart.get($(this).attr("data-series"));
    var series_button = $(this).find(".series-option");
    var error = chart.get($(this).attr("data-error-series"));
    var error_button = $(this).find(".error-option");
    if (series_button.hasClass("off")) {
      series.hide();
      error.hide();
    } else {
      series.show();
      if ((error_button.hasClass("off"))) {
        error.hide();
      } else {
        error.show();
      }
    }
  })
}

function makeChart(title, xMin, xMax, mainSeries, mainError, sampleScans, sampleErrors) {
  var series = [{
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
  for (var i = 0; i < sampleScans.length; i++) {
    series.push({
      data: sampleScans[i],
      id: "sample_" + (i + 1),
      color: COLORS[i],
      lineWidth: 1,
      visible: false,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false
          }
        }
      }
    })
  }
  for (var i = 0; i < sampleErrors.length; i++) {
    series.push({
      data: sampleErrors[i],
      id: "sample_error_" + (i + 1),
      type: "arearange",
      color: COLORS[i],
      fillOpacity: 0.2,
      lineWidth: 0,
      enableMouseTracking: false,
      visible: false
    })
  }
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
        enabled: true,
        headerFormat: '<span style="padding:0">{point.x} nm<br></span>',
        pointFormat: '<span style="padding:0"><b>{point.y:.2f}</b></span>',
      },
      series: series
    });
    return chart;
}


// When the page has finished loading...
$( document ).ready(function() {
  // Scroll to the top of the chart
  $("html, body").animate({
    scrollTop: $("#chart").offset().top
  }, 800);

  // Add event handlers for all the series config buttons
  $(".series-config").each(function() {
    var series_button = $(this).find(".series-option");
    var error_button = $(this).find(".error-option");

    series_button.click(function () {
      if ($(this).hasClass("on")) {
        console.log("Turning off")
        $(this).addClass("off").removeClass("on");
      } else {
        $(this).addClass("on").removeClass("off");
      }
      updateSeries();
    });

    error_button.click(function () {
      if ($(this).hasClass("on")) {
        $(this).addClass("off").removeClass("on");
      } else {
        $(this).addClass("on").removeClass("off");
      }
      updateSeries();
    });
  })

  // Add an event handler for the sample series button
  $("#sample-series-option").click(function () {
    if ($("#sample-series-option").hasClass("on")) {
      $("#sample-series-option").addClass("off").removeClass("on");
      $("#sample-scan-config").find(".series-config").each(function() {
        $(this).find("button").each(function() {
          $(this).addClass("off").removeClass("on");
        })
      })
    } else {
      $("#sample-series-option").addClass("on").removeClass("off");
      $("#sample-scan-config").find(".series-config").each(function() {
        $(this).find("button").each(function() {
          $(this).addClass("on").removeClass("off");
        })
      })
    }
    updateSeries();
  });
});
