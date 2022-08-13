$.ajax({
  type: 'GET',
  url: 'http://127.0.0.1:5000/get_data_compstacklineChart',
  success: function (response) {
    var objectData = response;
    console.log(objectData, typeof objectData);

    var dataSumbuX = objectData.datetime;
    var dataSumbuYday = objectData.kwhdclus;
    var dataSumbuYvday = objectData.kwhvdclus;
    var dataSumbuYmonth = objectData.kwhmclus;
    var dataSumbuYvmonth = objectData.kwhvmclus;
    var dataSumbuYyear = objectData.kwhyclus;
    var dataSumbuYvyear = objectData.kwhvyclus;

    buatCompLineChart(dataSumbuX, dataSumbuYday, dataSumbuYvday, dataSumbuYmonth, dataSumbuYvmonth, dataSumbuYyear, dataSumbuYvyear);
  },
});

var dougnutChart = echarts.init(document.getElementById("pieDoughnutChart"));

var option = {
  tooltip: {
    trigger: "item",
  },
  legend: {
    top: "5%",
    left: "center",
  },
  series: [
    {
      name: "Access From",
      type: "pie",
      radius: ["40%", "70%"],
      avoidLabelOverlap: false,
      label: {
        show: false,
        position: "center",
      },
      emphasis: {
        label: {
          show: true,
          fontSize: "40",
          fontWeight: "bold",
        },
      },
      labelLine: {
        show: false,
      },
      data: [
        { value: 735, name: "Tinggi" },
        { value: 580, name: "Normal" },
        { value: 300, name: "Rendah" },
      ],
    },
  ],
  responsive: true,
};

dougnutChart.setOption(option);
