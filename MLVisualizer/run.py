import os
import sys
import json
import time
import datetime
import random
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from gevent import Timeout
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

try:
    from visualizer.conf import *
    from visualizer.module import *
except:
    from conf import *
    from module import *

app = Flask(__name__)

#-- Error Handler
@app.errorhandler(500)
def error_handler(err):
    response = jsonify({ 'message': err.name, 'result': err.code })
    return response, err.code


#-- Application
@app.route('/')
def visualizer():
    socket_host = get_ec2_ip()
    log  = get_logfiles()
    html = render_template('index.html', HOST=socket_host, PORT=port, LOG=adjust_c3(log))
    return html
 

@app.route('/socket')
def socket():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        app.logger.info('Connection Start.')
        log = get_logfiles()
        try:
            while True:
                with Timeout(frequency, False):
                    msg = ws.receive()
                    if msg == 'closed':
                        break
                diff_log = get_diff_logfiles(log)
                log = get_logfiles()
                if diff_log is not None:
                    app.logger.info(diff_log)
                    ws.send(json.dumps(adjust_c3(log)))
                    app.logger.info('Sent to Web Socket!')
        except Exception as e:
            app.logger.error(e.args)
        finally:
            app.logger.info('Connection Closed.')
            ws.close()
    
    return 'Closed.'

@app.route('/parameters')
def data():
    return get_parameter()


def main():
    handler = RotatingFileHandler(os.path.join(visualizer_home_path, 'var/flask.log'), maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.debug = debug
    server = pywsgi.WSGIServer((host, port), app, handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
