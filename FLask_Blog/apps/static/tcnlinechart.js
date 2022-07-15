$.ajax({
  type: 'GET',
  url: 'http://127.0.0.1:5000/get_data_tcnlineChart',
  success: function (responseTCN) {
    var objectData = responseTCN;
    // console.log(objectData, typeof objectData);
    // var select = Object.values(response)
    var dataSumbuX = objectData.DateTime;
    var dataSumbuY = objectData.Predictions;
    // var dataCoba = Object.values(select)
    // console.log(dataSumbuY)
    buatTCNLineChart(dataSumbuX, dataSumbuY);
  },
});

function buatTCNLineChart(dataSumbuX, dataSumbuY) {
  var lineChart = echarts.init(document.getElementById('tcnlineChart'));

  var option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
    },
    xAxis: {
      type: 'category',
      data: dataSumbuX,
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: dataSumbuY,
        type: 'line',
      },
    ],
    responsive: true,
  };

  lineChart.setOption(option);
}
