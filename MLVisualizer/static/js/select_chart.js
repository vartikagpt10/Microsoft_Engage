function select_chart(chart, show_data, hide_data) {
  chart.show(show_data, {withLegend: true});
  chart.hide(hide_data, {withLegend: true});
}
