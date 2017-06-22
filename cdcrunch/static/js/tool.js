function assignFileListener() {
	/*
		By Osvaldas Valutis, www.osvaldas.info
		Available for use under the MIT License
	*/
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

function makeChart(title, xMin, xMax, data) {
	var series = [];
	for (var i = 0; i < data.length; i++) {
		series.push({
			data: data[i].errors,
			id: "sample_error" + i,
			color: data[i].color,
			type: "arearange",
			fillOpacity: 0.2,
			lineWidth: 0,
			enableMouseTracking: false
		});
		series.push({
	    data: data[i].values,
	    id: "sample" + i,
	    color: data[i].color,
	    lineWidth: data[i].width,
	    marker: {
	      enabled: false,
	      states: {
	        hover: {
	          enabled: false
	        }
	      }
			}
    });
	}
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

$( document ).ready(function() {
  // Scroll to the top of the chart
	if ($("#chart").length) {
	  $("html, body").animate({
	    scrollTop: $("#chart").offset().top
	  }, 800);
	}
	assignFileListener();
});
