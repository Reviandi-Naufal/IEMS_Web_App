$.ajax({
  type: 'GET',
  url: 'https://iems-telu.ismailab.xyz/get_data_clusteringVGdNPerhari',
  success: function (response) {
    var objectData = response;
    console.log(objectData, typeof objectData);

    var Normal = objectData.Normal;
    var Rendah = objectData.Rendah;
    var Tinggi = objectData.Tinggi;

    buatvgdNperhari(Normal, Rendah, Tinggi);
  },
});

function buatvgdNperhari(Normal, Rendah, Tinggi) {
  var dougnutChart = echarts.init(document.getElementById('pieDoughnutChartVH'));

  var option = {
    title: {
      text: 'Klaster Perhari',
      subtext: 'Gedung N',
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
          { value: Tinggi, name: 'Tinggi', color: '#FFF' },
          { value: Normal, name: 'Normal' },
          { value: Rendah, name: 'Rendah' },
        ],
      },
    ],
    responsive: true,
  };

  dougnutChart.setOption(option);
}
