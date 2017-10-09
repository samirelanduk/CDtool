function assignFileListener() {
	/*
		By Osvaldas Valutis, www.osvaldas.info
		Available for use under the MIT License
	*/
	// This function deals with the fancy file inputs
	var inputs = document.querySelectorAll("input[type=file]");
	Array.prototype.forEach.call(inputs, function(input) {
		var label	 = input.nextElementSibling, labelVal = label.innerHTML;
		input.addEventListener("change", function(e) {
			var fileName = "";
			if (this.files && this.files.length > 1)
				fileName = (this.getAttribute("data-multiple-caption") || "").replace(
					 "{count}", this.files.length
				);
			else
				fileName = e.target.value.split("\\").pop();
			if(fileName)
				label.innerHTML = fileName;
			else
				label.innerHTML = labelVal;
			});
	});
}


function makeChart(title, data) {
	/* Creates the Hghcharts chart from the data given to it */

	// Set up series objects
	var series = [];

	// Add the series' main line
	series.push({
		data: data.error,
		id: "sample_error",
		color: data.color,
		type: "arearange",
		fillOpacity: 0.2,
		lineWidth: 0,
		enableMouseTracking: false,
		zIndex: 99
	});
	series.push({
    data: data.series,
    id: "sample",
    color: data.color,
    lineWidth: data.linewidth,
    marker: {
      enabled: false,
      states: {hover: {enabled: false}}
		},
		zIndex: 100
  });

	// Add any component scans
	for (var s = 0; s < data.scans.length; s++) {
		series.push({
			data: data.scans[s].error,
			id: "sample_scan_" + s + "_error",
			color: data.scans[s].color,
			type: "arearange",
			fillOpacity: 0.2,
			lineWidth: 0,
			enableMouseTracking: false,
			zIndex: 99,
			visible: false
		});
		series.push({
	    data: data.scans[s].series,
	    id: "sample_scan_" + s,
	    color: data.scans[s].color,
	    lineWidth: data.scans[s].linewidth,
	    marker: {
	      enabled: false,
	      states: {hover: {enabled: false}}
			},
			zIndex: 100,
			visible: false
    });
	}

	// Create the chart
	var chart = Highcharts.chart("chart", {
		title: {
			text: title
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
      min: data.series[0][0],
      max: data.series[data.series.length - 1][0],
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


function toggleButton(button) {
	if ($(button).hasClass("on")) {
		$(button).addClass("off").removeClass("on");
	} else {
		$(button).addClass("on").removeClass("off");
	}
}

function submitDownload() {
	$("#download").find('input[name=series]').val(JSON.stringify(sample));
	return true;
}

$(document).ready(function() {
  // Scroll to the top of the chart
	if ($("#chart").length) {
	  $("html, body").animate({
	    scrollTop: $("#chart").offset().top
	  }, 800);
	}

	// Assign file input listeners
	assignFileListener();

	// Make show-more button work
	$(".show-more").click(function() {
		$(".scans-config").slideToggle("fast");
	});

	// Add event handlers for all the series config buttons
  $(".series-option").each(function() {
    $(this).click(function () {
      toggleButton(this);
			var nextButton = $(this).next("button");
			var series = chart.get($(this).attr("data-series"));
			var errorSeries = chart.get($(nextButton).attr("data-series"));
			if ($(this).hasClass("off")) {
	      series.hide();
				errorSeries.hide();
	    } else {
	      series.show();
				if ($(nextButton).hasClass("on")) {
					errorSeries.show();
				}
	    }
    });
	});

	// Add event handlers for all the series error config buttons
  $(".error-option").each(function() {
    $(this).click(function () {
      toggleButton(this);
			var previousButton = $(this).prev("button");
			var series = chart.get($(this).attr("data-series"));
			var masterSeries = chart.get($(previousButton).attr("data-series"));
			if ($(this).hasClass("off")) {
	      series.hide();
	    } else {
				if ($(previousButton).hasClass("on")) {
					series.show();
				}
	    }
		});
	});

	// Add event handlers for all multi-scan toggles
	$(".multi-scan-toggle").each(function() {
		$(this).click(function() {
			toggleButton(this);
			var visible = $(this).hasClass("on");
			var buttons = $(this).parent().find(".series-button");
			buttons.each(function() {
				var series = chart.get($(this).attr("data-series"));
				if (visible) {
					$(this).addClass("on").removeClass("off");
					series.show();
				} else {
					$(this).addClass("off").removeClass("on");
					series.hide();
				}
			});
		})
	});

});
