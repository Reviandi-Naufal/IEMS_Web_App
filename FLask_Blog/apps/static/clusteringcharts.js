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
