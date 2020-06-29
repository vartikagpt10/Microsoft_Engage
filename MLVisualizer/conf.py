import os

# ============================== #
# CONFIG
# ============================== #
visualizer_home_path = '/data/visualizer/' # Visualizer application's path
log_path       = os.path.join(visualizer_home_path, 'logfiles')
parameter_path = os.path.join(visualizer_home_path, 'logfiles')
run_path       = os.path.join(visualizer_home_path, 'run.py')
flask_log      = os.path.join(visualizer_home_path, 'var/flask.log')

host      = '0.0.0.0'
port      = 8889
debug     = False # Flask debug mode
frequency = 1.0 # Log rendering frequency(sec.)

