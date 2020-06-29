import os
import re
import sys
import datetime
import subprocess
import textwrap
import pandas as pd
from flask import abort
try:
    from visualizer.conf import *
except:
    from conf import *

# ========== -- General
def get_ec2_ip():
    '''
    Fetch the IP address of running ec2
    '''
    return subprocess.check_output(["curl","-q","http://169.254.169.254/latest/meta-data/public-ipv4"]).decode('utf8')


# ========== -- Error Handle
def err_handle(err):
    '''
    error handling
    '''
    abort(500, { 'message': err })


# ============================== #
# User Modules
# ============================== #
    

# ========== -- ログを保存する -- ========== #
def set_param_name(prefix='', suffix='', strf='%Y%m%d-%H%M'):
    '''
    Determine file name of hyper　parameter from prefix and suffix
    '''
    if prefix != '':
        prefix = prefix + '_'
    if suffix != '':
        suffix = '_' + suffix
    name  = prefix + datetime.datetime.now().strftime(strf) + suffix + '.json'
    return name


def set_log_name(title, mode='loss'):
    '''
    Determine the log name
    '''
    name = title + '_' + mode + '.log'
    return name


def set_regex_log_name(log, regex, delimiter=None):
    hashlog = re.findall(regex,logs)
    if delimiter is not None:
        strlog = hashlog.join(delimiter)
    else:
        strlog = hashlog
    return strlog


def write_linelog(file_path, linelog):
    '''
    Export logs line by line
    '''
    if type(linelog) is not list:
        linelog = [linelog]
    dflog = pd.DataFrame(linelog)
    if debug:
        print(dflog)
    else:
        dflog.to_csv(file_path, mode='a', header=False, index=False)


def write_strlog(path, strlog):
    '''
    Export multi-line logs collectively
    '''
    dflog = pd.DataFrame(strlog)
    if debug:
        print(dflog)
    else:
        dflog.to_csv(path, header=False, index=False)


#-- Hyper Parameter
def set_hyperparameter(title=None, prefix='', suffix='', param=None):
    '''
    USAGE:
    title = set_hyperparameter(title=None, prefix='', suffix='', param)
    - title: 保存するログのファイル名
    - prefix, suffix: 保存するログのファイル名. titleを指定しない場合はこちらが採用される.
    ex.) prefix_%Y%m%d-%H%M_suffix.json
    
    ※title, prefix, suffixいずれも指定しない場合は, %Y%m%d-%H%M.jsonで保存される.
    
    - param: 保存したいパラメータを辞書型で保存
    ex.) {'epoch': 100, 'batch_size': 32, 'initial_lr': 0.01, 'optim': 'Adam'}
    '''
    try:
        file_name = set_param_name(prefix=prefix, suffix=suffix)
        file_ = os.path.join(parameter_path, file_name)
        if title is None:
            title = file_name.replace('.json', '')
        assert param != ''
        se_parameter = pd.Series(dict({'title': title}, **param))
        if debug:
            print(textwrap.dedent('''\
                debug mode is True.
                if you changed debug mode, you can change it at conf.py!!
                '''))
        else:
            print(textwrap.dedent(f'''\
                debug mode is False.
                saving Hyper Parameter data {file_}
                '''))
            se_parameter.to_json(file_)
    except:
        print('''
        Error!!
        Prease read set_hyperparameter.__doc__
        '''
        )
    return title

#-- Logs
def set_log(log, title, mode='loss', how_to_write='line'):
    '''
    USAGE:
    set_logfiles(log, title, mode='loss')
    - log: 保存するlogデータ.
    - title: set_hyperparameterの戻り値を設定
    - mode = 'loss': lossモード
    - mode = 'metric' : metricモード
    - mode = 'lr'  : learning rateモード
    '''
    try:
        assert mode in ['loss', 'metric', 'lr']
        file_name = set_log_name(title, mode=mode)

        file_ = os.path.join(log_path, file_name)
        if how_to_write == 'line':
            write_linelog(file_, log)
        elif how_to_write == 'str':
            write_strlog(file_, log)
        else:
            print('writing log error.')
            raise Exception
    except:
        print('''
        Error!!
        Prease read set_log.__doc__
        '''
        )

# ============================== #
# System Modules
# ============================== #
### logディレクトリにあるログファイルを読み込む
def get_filelist(flist_path, mode='log'):
    '''
    Return the file list of flist_path
    '''
    try:
        file_list = [os.path.join(flist_path, x) for x in os.listdir(flist_path) if os.path.isfile(os.path.join(flist_path, x))]
        file_list = [f for f in file_list if '.'+mode in f ]
    except:
        file_list = None
    return file_list


# ========== -- hyper parametersの取得 -- ========== #
def get_parameter():
    '''
    Convert hyper parameter to json format and return summary
    '''
    try:
        filelist   = get_filelist(parameter_path, mode='json')
        if len(filelist) > 1:
            parameters = [pd.read_json(f, typ='series', orient='records') for f in filelist]
            parameters = [pd.Series(p) for p in parameters]
            df = parameters[0]
            for p in parameters[1:]:
                df = pd.concat([df, p], axis=1, ignore_index=True)
            param_json = df.fillna('NULL').T.to_json(orient='records')
        else:
            parameters = pd.read_json(filelist[0], typ='series', orient='records') 
            parameters = pd.Series(parameters)
            param_json = parameters.T.to_json()
    except:
        param_json = None
    return param_json


def get_architectual_parameter():
    '''
    Read hyper parameter file list of parameter_path you set in conf.py
    merge all json file
    return json
    '''
    try:
        filelist   = get_filelist(parameter_path, mode='json')
        parameters = [pd.read_json(f, typ='series', orient='records') for f in filelist]
        parameters = [pd.DataFrame(p).T.set_index('title').T for p in parameters]
        df = parameters[0]
        for p in parameters[1:]:
            df = pd.concat([df, p], axis=1)
        param_json = df.to_json()
    except:
        print('err')
        param_json = None
    return param_json


# ========== -- Log Dataの取得 -- ========== #
### logのリストデータをグラフ描画に合わせたdict型へ変換する
def make_dict(data):
    '''
    Convert list to dictionaly
    ex.) [0.5,0.4,0.3] -> [{x:1, y:0.5}, {x:2, y:0.4}, {x:3, y:0.3}] 
    '''
    arr_length = len(data)
    x_keys = ['x'] * arr_length
    y_keys = ['y'] * arr_length
    x_axis = [i for i in range(1, arr_length + 1)]
    return [{k_x: v_x, k_y: v_y} for (k_x, v_x, k_y, v_y) in zip(x_keys, x_axis, y_keys, data)]


def make_dict_wrapper(log_data):
    log_data = [{k: make_dict(v)} if '.log' in k else {k: v} for l_data in log_data for k, v in l_data.items()]
    return log_data


def adjust_c3(data):
    '''
    Adjust c3 data format
    ex.) [{'hoge.log': [0,1,2,3]}, {'fuga.log': [1,2,3,4]}]
         -> [['hoge.log',0,1,2,3], ['fuga.log',1,2,3,4]]
    '''
    adjust_data = []
    for dict_ in data:
        for k, v in dict_.items():
            adjust_data.append([k] + v)
    return adjust_data


def get_data(file_path):
    '''
    Read csv data of file_path and return it as an array
    '''
    with open(file_path, "r") as f:
        data = [line.rstrip() for line in f]
    data = [d.split(',') if ',' in d else d for d in data]
    return {os.path.basename(file_path): data}


def get_logfiles():
    '''
    Read all the file list of log_path you set in conf.py and return it as an array
    log_path you set in conf.py
    '''
    try:
        filelist = get_filelist(log_path, mode='log')
        log_data = [get_data(l) for l in filelist]
    except:
        print('err')
        log_data = None
    return log_data


### 既に取得しているログと新しく取得したログの差分を返す
def get_diff(list2, list1):
    '''
    return difference of list
    list2 > list1
    '''
    result = list1.copy()
    for value in list2:
        if value in result:
            result.remove(value)
    return result


def check_update(diff_data):
    '''
    Check whether the log has been updated
    '''
    is_update = False
    for data in diff_data:
        d = [v for v in data.values()]
        if d[0] != []:
            is_update = True
            break
    return is_update


def get_diff_logfiles(source_data):
    '''
    Get the log update difference
    '''
    try:
        # 新規ファイル(new_filelist)と新規ファイルのデータ(new_file_data)を取得
        source_filelist = [os.path.join(log_path, d) for data in source_data for d in data.keys()]
        cur_filelist    = get_filelist(log_path, mode='log')
        new_filelist    = get_diff(source_filelist,  cur_filelist)
        new_file_data   = [get_data(l) for l in new_filelist]
        
        # 既存ファイルの差分データ(diff_data)を取得する
        diff_data     = []
        for cd, sd in zip([get_data(cf) for cf in cur_filelist], source_data):
            key  = [k for k in cd.keys()]
            v_cd = [v for v in cd.values()]
            v_sd = [v for v in sd.values()]
            diff_data.append({key[0]: get_diff(v_sd[0], v_cd[0])})
        if new_file_data != []:
            diff_data.extend(new_file_data)
        if not check_update(diff_data):
            raise Exception
    except:
        diff_data = None
    return diff_data
        
        
