function sort_colors(chart, mode) {
  var color_dict = chart.data.colors();
  var sorted_color_dict = {};
  var data = [];
  var colors = [];
  for (key in color_dict) {
    data.push(key);
    colors.push(color_dict[key]);
  }
  data.sort();
  colors.sort();
  var obj = Object.create(null);
  for (var i = 0, l = data.length,obj; i < l; ++i) {
    if (colors.hasOwnProperty(i)) {
      obj[data[i]] = colors[i];
    }
  }

  var replaced_obj = Object.create(null);
  for (o in obj) {
    if (mode === 'loss') {
      replaced_obj[o.replace(/(loss|metric|lr)\.log/g, 'loss.log')] = obj[o];
    }
    else if (mode === 'metric') {
      replaced_obj[o.replace(/(loss|metric|lr)\.log/g, 'acc.log')] = obj[o];
    }
    else if (mode === 'lr') {
      replaced_obj[o.replace(/(loss|metric|lr)\.log/g, 'lr.log')] = obj[o];
    }
  }
  return replaced_obj;
}
