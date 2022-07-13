$.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/get_data_lineChart",
    success: function (response) {
      var objectKwh = response
      console.log(
        objectKwh,
        typeof(objectKwh)
      )
      var select = Object.values(response)
      var dataSumbuX = Object.keys(select)
      var dataSumbuY = Object.values(select.Date)
      var dataCoba = Object.values(select)
      console.log(dataSumbuY)
      buatLineChart(dataSumbuX, dataSumbuY)
      
    }
})

function buatLineChart(dataSumbuX, dataSumbuY) {
  var lineChart = echarts.init(
      document.getElementById("lineChart")
  )

  var option = {
    tooltip:{
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: dataSumbuX
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: dataSumbuY,
        type: 'line'
      }
    ]
  }

  lineChart.setOption(option)
}