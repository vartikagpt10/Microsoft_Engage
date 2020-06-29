function split_log(log_data, mode) {
  var loss = [];
  var metric  = [];
  var lr   = [];
  log_data.forEach(function(data) {
    if(data[0].indexOf('loss.log') != -1) {
      if (mode === 'data') {
        loss.push(data);
      }
      else if (mode === 'list') {
        loss.push(data[0]);
      }
    }
    else if(data[0].indexOf('metric.log') != -1) {
      if (mode === 'data') {
        metric.push(data);
      }
      else if (mode === 'list') {
        metric.push(data[0]);
      }
    }
    else if(data[0].indexOf('lr.log') != -1) {
      if (mode === 'data') {
        lr.push(data);
      }
       else if (mode === 'list') {
        lr.push(data[0]);
      }
    }
    else {
      console.log('Wrong log name:'+data[0]);
    }
  });
  return [loss, metric, lr];
}

