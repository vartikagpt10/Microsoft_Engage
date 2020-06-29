# ML Visualizer

pytorchのログを保存して可視化する.

## Getting Started

### 準備

1. git cloneしてくる
2. conf.pyの設定

```
visualizer_home_path = '/data/visualizer/' # <-ここにcloneしてきたML Visualizerのpath
log_path       = os.path.join(visualizer_home_path, 'logfiles')
parameter_path = os.path.join(visualizer_home_path, 'logfiles')
run_path       = os.path.join(visualizer_home_path, 'run.py')
flask_log      = os.path.join(visualizer_home_path, 'var/flask.log')

host      = '0.0.0.0'
port      = 8889 # <- ここでport指定
debug     = False
frequency = 1.0 # socketで通信する間隔(いじらなくてもよい)
```


3. 依存パッケージのインストール

```
flaskとかgeventsocketとか、必要があれば
```

### 起動

1. flaskを起動する
```
$ python run.py
```

2. ブラウザから、"サーバのIP:指定したポート" でアクセス

### ログの保存

1. pytorchのアプリケーションにimportする

```
pathを通してから
from visualizer import module
```

2. hyper parameterの保存

```
param = {'epoch':10, 'batch':100, 'optimizer':'SGD'}
hyper_parameters = module.set_hyperparameter(prefix='mnist', param=param)

--
- prefixを指定すると「prefix_%Y%m%d-%H%M」形式でログが保存される
- パラメータはdict型で指定
```


3. ログの保存

```
module.set_log(log, hyper_parameters, mode='loss')

--
- 第1引数に保存したいログ
- 第2引数にmodule.set_hyperparameterの戻り値(logのファイル名)
- 第3引数にmode= loss, acc, lrから指定
```

4. 可視化

![可視化](https://github.com/ysdtsy/ml_visualizer/blob/master/images/screen1.png)


## Directory Structure

```
├── conf.py #pathとflaskの設定ファイル
├── images #git用(appには不要)
│   └── screen1.png
├── __init__.py
├── logfiles
│   └── #ここにログが保存される
├── module.py #バックエンド側のmoduleが格納
├── README.md
├── requirements.txt #参考程度に
├── run.py #flaskのルーティング設定兼起動ファイル
├── static #静的ファイル格納ディレクトリ
│   ├── css
│   │   ├── c3_style.css #c3.js用
│   │   ├── decolate_style.css #.htmlのデザイン全般
│   │   ├── layout.css #.htmlのレイアウト全般
│   │   └── table_style.css #hyper parametersのテーブル用
│   ├── dist #外部ライブラリ格納用
│   │   ├── css
│   │   │   └── c3.min.css #c3.jsのライブラリcss
│   │   └── js
│   │       └── c3.min.js #c3.jsのライブラリjs
│   ├── favicon.ico
│   ├── images #.htmlの画像用
│   └── js #フロント側のmoduleが格納
│       ├── draw_chart.js #グラフ描画
│       ├── get_json.js #hyoer parameterのjson取得
│       ├── get_show_or_hide.js #グラフの非表示のリストを取得
│       ├── json_to_table.js #jsonデータをhtmlテーブルに変換
│       ├── select_chart.js #グラフの非表示をグラフに適用
│       ├── sort_colors.js #グラフの色を設定
│       └── split_log.js #ログをloss acc lrに分割する
├── templates
│   └── index.html #htmlページ
└── var
    └── flask.log #flaskのログが格納
```


## Authors

* **Toshiya Yoshida** - *at D2C Inc.*
