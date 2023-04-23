var DATA_ITEMS = 60; // 5' x 60'' / 5''

function getLabelIndex(datasets, label) {
  for (let i = 0; i < datasets.length; i++) {
    if (label == datasets[i].label) {
      return i;
    }
  }

  return -1;
}

var next_color_idx = 0;
var colors = Object.values(window.chartColors);
function getColor() {
  cidx = next_color_idx;
  next_color_idx = (next_color_idx + 1) % colors.length;
  return colors[cidx];
}

function getSecondsInCurrentMinute() {
  const now = new Date();
  return now.getSeconds();
}

function createList() {
  const list = new Array(60).fill(-1);
  return list;
}

function update_chart(chart, data) {
  const myList = createList();
  current_labels = [];
  for (let i = 0; i < chart.config.data.datasets.length; i++) {
    dataset = chart.config.data.datasets[i];
    if (dataset.data.length <= 1) {
      chart.config.data.datasets.splice(i, 1); // remove item
    } else {
      current_labels.push(dataset.label);
      dataset.data.shift();
    }
  }

  data_labels = Object.keys(data);
  new_labels = data_labels.filter((label) => !current_labels.includes(label));

  // update label list
  chart.config.data.labels.shift();
  chart.config.data.labels.push(getSecondsInCurrentMinute());

  // update current labels
  for (let i = 0; i < current_labels.length; i++) {
    label = current_labels[i];
    idx = getLabelIndex(chart.config.data.datasets, label);
    chart.config.data.datasets[idx].data.push(data[label]);
  }

  // create new labels
  for (let i = 0; i < new_labels.length; i++) {
    label = new_labels[i];
    color = getColor();
    let new_class = {
      label: label,
      fill: false,
      backgroundColor: color,
      borderColor: color,
      data: new Array(59).fill(0),
    };
    new_class.data.push(data[label]);
    chart.config.data.datasets.push(new_class);
  }
  chart.update();
}

var chart_config = {
  type: "line",
  data: {
    labels: new Array(DATA_ITEMS).fill(""),
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
