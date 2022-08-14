$.ajax({
  type: 'GET',
  url: 'http://127.0.0.1:5000/get_data_clusteringgdNPertahun',
  success: function (response) {
    var objectData = response;
    console.log(objectData, typeof objectData);
    var Normal = objectData.Normal;
    var Rendah = objectData.Rendah;
    var Tinggi = objectData.Tinggi;

    buatgdNpertahun(Normal, Rendah, Tinggi);
  },
});

function buatgdNpertahun(Normal, Rendah, Tinggi) {
  var dougnutChart = echarts.init(document.getElementById('pieDoughnutChartVT'));

  var option = {
    tooltip: {
      trigger: 'item',
    },
    legend: {
      top: '5%',
      left: 'center',
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '40',
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
        data: [
          { value: Tinggi, name: 'Tinggi' },
          { value: Normal, name: 'Normal' },
          { value: Rendah, name: 'Rendah' },
        ],
      },
    ],
    responsive: true,
  };

  dougnutChart.setOption(option);
}
