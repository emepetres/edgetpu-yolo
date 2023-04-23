var DATA_ITEMS = 30; // 2.5' x 60'' / 5''

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

function update_chart(chart, data) {
  data_labels = Object.keys(data);
  current_labels = {};
  old_labels = {};
  for (let i = 0; i < chart.config.data.datasets.length; i++) {
    let dataset = chart.config.data.datasets[i];
    if (data_labels.includes(dataset.label)) {
      current_labels[dataset.label] = [i, dataset];
    } else {
      old_labels[dataset.label] = [i, dataset];
    }
  }

  // update current registries
  for (let label in current_labels) {
    let dataset = current_labels[label][1];
    dataset.data.shift();
    dataset.data.push(data[label]);
  }

  // update old registries
  let old_classes_to_delete = [];
  for (let label in old_labels) {
    let dataset = old_labels[label][1];
    dataset.data.shift();
    dataset.data.push(NaN);
    if (dataset.data.every(isNaN)) {
      let idx = old_labels[label][0];
      old_classes_to_delete.push(idx);
    }
  }

  // add new label on x axes
  chart.config.data.labels.shift();
  chart.config.data.labels.push(getSecondsInCurrentMinute());

  // delete too old registries
  old_classes_to_delete.sort(function (a, b) {
    return a - b;
  });
  for (let i = 0; i < old_classes_to_delete.length; i++) {
    let idx = old_classes_to_delete[i] - i;
    chart.config.data.datasets.splice(idx, 1); // remove class
  }

  // create new classes
  let current_labels_list = Object.keys(current_labels);
  let new_labels = data_labels.filter(
    (label) => !current_labels_list.includes(label)
  );
  for (let i = 0; i < new_labels.length; i++) {
    let label = new_labels[i];
    let color = getColor();
    let new_class = {
      label: label,
      fill: false,
      backgroundColor: color,
      borderColor: color,
      pointRadius: 0,
      data: new Array(DATA_ITEMS - 2).fill(NaN),
    };
    new_class.data.push(0);
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
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  },
};
