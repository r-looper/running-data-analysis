# Garmin ランニングデータ可視化（Python）

GarminのアクティビティCSVを読み込み、**距離・平均ペース・平均心拍数**を可視化するPythonスクリプトです。  
クラウドワークスのポートフォリオ用に公開しています。

---

## 機能
- 日付ごとの **距離 (km)** を折れ線グラフ化  
- **平均ペース**を数値に変換し、`分/㎞` 表示でグラフ化  
- **平均心拍数 (bpm)** の推移を可視化（列がある場合）  
- グラフはPNG画像として保存されます（`images/` フォルダに出力）

---

## サンプルデータについて
- プライバシー保護のため、このリポジトリには **公開用のサンプルデータ** (`sample_running_data.csv`) を同梱しています。  
- 実際の個人データ (`Activities.csv`) は含まれていません。  
- 自分のGarmin CSVを利用したい場合は、`main.py` の以下を修正してください：

```python
CSV_PATH = "sample_running_data.csv"  # 公開用サンプル
# 実際に使うときは ↓ に置き換え
# CSV_PATH = "Activities.csv"


必要環境
Python 3.11 以上
必要ライブラリ：pandas, matplotlib
インストール方法：pip install pandas matplotlib


実行方法
CSVファイル（例：sample_running_data.csv）を同じフォルダに置く
main.py を実行
images/ フォルダに以下の画像が生成されます：
distance.png（距離の推移）
pace.png（平均ペースの推移）
heart_rate.png（平均心拍数の推移、列がある場合）

注意
このリポジトリはポートフォリオ用です。
公開しているCSVはダミーデータであり、個人の走行記録は含まれていません。


