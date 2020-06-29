function draw_chart(bindto, data) {
  var chart = c3.generate({
    bindto: bindto,
    data: {
      columns: data
    },
    grid: {
      x: {
        show: true
      },
      y: {
        show: true
      }
    },
    axis: {
      y: {
        label: {
          text: '',
          position: 'outer-middle'
        }
      }
    },
    zoom: {
      enabled: true,
      type: 'drag'
    }
  });
  return chart;
}
