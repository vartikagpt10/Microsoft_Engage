function json_to_table(data) {
  /* creating table header */
  var tbl_head = '';
  var tbl_body = '';
  var odd_even = false;
  var title_id = 0;
  if (!(data instanceof Array)) {
    var value = data;
    var data = [];
    data.push(value);
  }

  $.each(data, function() {
    var tbl_row  = '';
    var col_count = 0;
    $.each(this, function(k , v) {
      tbl_row += "<th>"+k+"</th>";
      if (k === 'title') {
        title_id = col_count;
      }
      col_count += 1;
    });
    tbl_head = "<tr><th></th>"+tbl_row+"</tr>";            
  });

  /* creating table bodies */
  $.each(data, function() {
    var tbl_row = '';
    var title_name = '';
    var col_count = 0;
    $.each(this, function(k , v) {
      tbl_row += "<td>"+v+"</td>";
      if (col_count === title_id) {
        title_name = v;
      }
      col_count += 1;
    });
    tbl_body += "<tr class=\""+( odd_even ? "odd" : "even")+"\"><td><input id=\""+title_name+"\" class=\"checkbox\" name=\"parameters\" type=\"checkbox\" value=\""+title_name+"\" /></td>"+tbl_row+"</tr>";
    odd_even = !odd_even;               
  });
  return [tbl_head, tbl_body]
}

