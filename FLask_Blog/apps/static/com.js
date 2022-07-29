$.ajax({
  type: 'GET',
  url: 'https://iems-telu.ismailab.xyz/get_data_grulineChart',
  url: 'https://iems-telu.ismailab.xyz/get_data_rnnlineChart',
  success: function (response) {
    var objectData = response;
    console.log(objectData, typeof objectData);

    var dataSumbuXgru = objectData.datetime;
    var dataSumbuYgru = objectData.Kwh;

    buatCompLineChart(dataSumbuXgru, dataSumbuYgru);
  },
});

function senddatagru() {
  $.ajax({
    type: 'POST',
    url: 'https://iems-telu.ismailab.xyz/get_data_grulineChart',
    success: function (response) {
      var objectData = response;
      console.log(objectData, typeof objectData);

      var dataSumbuXgru = objectData.datetime;
      var dataSumbuYgru = objectData.Kwh;

      buatCompLineChart(dataSumbuXgru, dataSumbuYgru);
    },
  });
}

function buatCompLineChart(dataSumbuX, dataSumbuY) {
  var stacked_line = echarts.init(document.getElementById('comlineChart'));

  var option = {
    title: {
      text: 'Algorithm Compare',
    },
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: ['RNN', 'GRU', 'LMU', 'TCN'],
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    toolbox: {
      feature: {
        saveAsImage: {},
      },
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dataSumbuX,
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: 'RNN',
        type: 'line',
        stack: 'Total',
        data: dataSumbuYrnn,
      },
      {
        name: 'GRU',
        type: 'line',
        stack: 'Total',
        data: dataSumbuYgru,
      },
      {
        name: 'LMU',
        type: 'line',
        stack: 'Total',
        data: dataSumbuYlmu,
      },
      {
        name: 'TCN',
        type: 'line',
        stack: 'Total',
        data: dataSumbuYtcn,
      },
    ],
    responsive: true,
  };

  stacked_line.setOption(option);
}
