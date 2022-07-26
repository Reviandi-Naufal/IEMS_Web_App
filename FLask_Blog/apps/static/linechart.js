$.ajax({
  type: "GET",
  url: "http://0.0.0.0:5000/get_data_lineChart",
  success: function (response) {
    var objectData = response;
    console.log(objectData, typeof objectData);
    // var select = Object.values(response)
    var dataSumbuX = objectData.datetime;
    var dataSumbuY = objectData.Kwh;
    // var dataCoba = Object.values(select)
    // console.log(dataSumbuY)
    buatLineChart(dataSumbuX, dataSumbuY);
  },
});

function buatLineChart(dataSumbuX, dataSumbuY) {
  var lineChart = echarts.init(document.getElementById("lineChart"));

  var option = {
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
    },
    xAxis: {
      type: "category",
      data: dataSumbuX,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: dataSumbuY,
        type: "line",
      },
    ],
    responsive: true,
  };

  lineChart.setOption(option);
}
