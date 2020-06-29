function get_show_or_hide(checked_id, logs, data) {
  var select_data = [];
  logs.forEach(function(l) {
    $(checked_id).each(function() {
      select_data.push($(this).val()+'_'+l+'.log');
    });
  });
  data_list = [];
  data.forEach(function(d) {
    data_list.push(d[0])
  });
  var show_data = data_list.concat(select_data).filter(function (x, i, self) {
    return self.indexOf(x) === i && i !== self.lastIndexOf(x);
  });
  var hide_data = show_data.concat(data_list).filter(function (x, i, self){
    return self.indexOf(x) === self.lastIndexOf(x);
  });
  return [show_data, hide_data];
}
