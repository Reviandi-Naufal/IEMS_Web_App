$.ajax({
  type: "GET",
  url: "https://iems-telu.ismailab.xyz/get_data_tcnlineChart",
  success: function (responseTCN) {
    var objectData = responseTCN;
    // console.log(objectData, typeof objectData);
    // var select = Object.values(response)
    var dataSumbuX = objectData.datetime;
    var dataSumbuY = objectData.Kwh;
    // var dataCoba = Object.values(select)
    // console.log(dataSumbuY)
    buatTCNLineChart(dataSumbuX, dataSumbuY);
  },
});

function buatTCNLineChart(dataSumbuX, dataSumbuY) {
  var TCNlineChart = echarts.init(document.getElementById("tcnlineChart"));

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

  TCNlineChart.setOption(option);
}
