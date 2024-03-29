$.ajax({
  type: 'GET',
  url: 'https://iems-telu.ismailab.xyz/get_data_grulineChart',
  success: function (response) {
    var objectData = response;
    console.log(objectData, typeof objectData);
    // var select = Object.values(response)
    var dataSumbuX = objectData.datetime;
    var dataSumbuY = objectData.Kwh;
    // var dataCoba = Object.values(select)
    // console.log(dataSumbuY)
    buatGRULineChart(dataSumbuX, dataSumbuY);
  },
});

function buatGRULineChart(dataSumbuX, dataSumbuY) {
  var lineChart = echarts.init(document.getElementById('grulineChart'));

  var option = {
    title: {
      text: 'Predictions Chart',
      left: '1%',
    },
    tooltip: {
      trigger: 'axis',
    },
    grid: {
      left: '5%',
      right: '15%',
      bottom: '10%',
    },
    xAxis: {
      data: dataSumbuX,
    },
    yAxis: {},
    toolbox: {
      right: 10,
      feature: {
        dataZoom: {
          yAxisIndex: 'none',
        },
        restore: {},
        saveAsImage: {},
      },
    },
    dataZoom: [
      {
        startValue: '2021-09-01',
      },
      {
        type: 'inside',
      },
    ],
    visualMap: {
      top: 50,
      right: 10,
      pieces: [
        {
          gt: 0,
          lte: 5,
          color: '#93CE07',
        },
        {
          gt: 5,
          lte: 10,
          color: '#FFF33B',
        },
        {
          gt: 10,
          lte: 15,
          color: '#FDC70C',
        },
        {
          gt: 15,
          lte: 20,
          color: '#F3903F',
        },
        {
          gt: 20,
          lte: 25,
          color: '#ED683C',
        },
        {
          gt: 25,
          color: '#C93C3A',
        },
      ],
      outOfRange: {
        color: '#999',
      },
    },
    series: {
      name: 'Predictions Chart',
      type: 'line',
      data: dataSumbuY,
      markLine: {
        silent: true,
        lineStyle: {
          color: '#799',
        },
        data: [
          {
            yAxis: 5,
          },
          {
            yAxis: 10,
          },
          {
            yAxis: 15,
          },
          {
            yAxis: 20,
          },
          {
            yAxis: 25,
          },
        ],
      },
    },
    responsive: true,
  };

  lineChart.setOption(option);
}
