var chart_config = {
  type: "line",
  data: {
    labels: [],
    datasets: [],
  },
  options: {
    animation: false,
    responsive: true,
    title: {
      display: true,
      text: "Data collected",
    },
    tooltips: {
      mode: "index",
      intersect: false,
    },
    hover: {
      mode: "nearest",
      intersect: true,
    },
    scales: {
      xAxes: [
        {
          display: true,
          scaleLabel: {
            display: true,
            labelString: "Time",
          },
        },
      ],
      yAxes: [
        {
          display: true,
          scaleLabel: {
            display: true,
            labelString: "#",
          },
        },
      ],
    },
  },
};
