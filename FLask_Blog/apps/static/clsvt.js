$.ajax({
  type: 'GET',
  url: 'https://iems-telu.ismailab.xyz/get_data_clusteringvgdNPertahun',
  success: function (response) {
    var objectData = response;
    console.log(objectData, typeof objectData);

    var Normal = objectData.Normal;
    var Rendah = objectData.Rendah;
    var Tinggi = objectData.Tinggi;

    buatvgdNpertahun(Normal, Rendah, Tinggi);
  },
});

function buatvgdNpertahun(Normal, Rendah, Tinggi) {
  var dougnutChart = echarts.init(document.getElementById('pieDoughnutChartVT'));

  var option = {
    title: {
      text: 'Klaster Pertahun',
      subtext: 'Silhouette Score: 0,72',
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c} ({d}%)',
    },
    legend: {
      bottom: '5%',
      left: 'center',
    },
    series: [
      {
        name: 'Cluster',
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
