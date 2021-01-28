# MH-Z14A-WebUI
NDIRCO2センサー MH-Z14A と Flask を利用した定期的な計測および簡易的な WebUI

#### サンプル

![](assets/ex1.png)

デフォルトで常に 5 分ごとに記録され，WebUI では 10 秒ごとに数値のみを更新，5分おきにグラフを更新します．



## 動作確認済み環境

* NanoPi NEO2
* MH-Z14A



## 準備

NanoPi から MH-Z14A の値を取れるように接続・設定する



## 実行
1. `$ pip install -r requirements.txt`
1. `$ python3 app.py`
1. http://localhost:5000 を開く



