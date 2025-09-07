import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ==== 設定：CSVの場所（実ファイル名に合わせる）====
CSV_PATH = "sample_running_data.csv"

# ==== 出力先：main.py と同じフォルダ配下の images/ ====
BASE_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(OUT_DIR, exist_ok=True)

def out(name: str) -> str:
    return os.path.join(OUT_DIR, name)

# ==== 読み込み ====
df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

# ==== 日付を時系列に ====
df["日付"] = pd.to_datetime(df["日付"], errors="coerce")
df = df.sort_values("日付")

# ==== 平均ペースを「分/㎞(float)」に正規化 ====
def parse_pace_to_min_per_km(x: str):
    if pd.isna(x):
        return None
    s = str(x).strip().replace("：", ":")
    s = re.sub(r"\s+", "", s)
    s = (s.replace("分／km", "").replace("分/km", "").replace("/km", "")
           .replace("min/km", "").replace("分", "").replace("／km", "")
           .replace("km", "").replace("／", "/"))
    if ":" in s:
        parts = s.split(":")
        try:
            if len(parts) == 2:   # mm:ss
                m = int(parts[0]); sec = float(parts[1])
                return m + sec/60.0
            elif len(parts) == 3: # hh:mm:ss
                h = int(parts[0]); m = int(parts[1]); sec = float(parts[2])
                return h*60 + m + sec/60.0
        except ValueError:
            pass
    try:
        return float(s)
    except ValueError:
        return None

df["pace_min_per_km"] = df["平均ペース"].apply(parse_pace_to_min_per_km)
plot_df = df.dropna(subset=["pace_min_per_km", "距離", "日付"])

# ==== 便利：y軸を M:SS 表示 ====
def mmss_formatter(y, _pos):
    m = int(y)
    s = int(round((y - m) * 60))
    if s == 60:
        m += 1; s = 0
    return f"{m}:{s:02d}"

# ==== 1) 距離 ====
plt.figure(figsize=(10, 5))
plt.plot(plot_df["日付"], plot_df["距離"], marker="o", linestyle="-")
plt.title("ランニング距離の推移")
plt.xlabel("日付")
plt.ylabel("距離 (km)")
plt.grid(True)
plt.tight_layout()
dist_path = out("distance.png")
plt.savefig(dist_path)
print("保存:", dist_path)
# plt.show()
plt.close()

# ==== 2) 平均ペース ====
plt.figure(figsize=(10, 5))
plt.plot(plot_df["日付"], plot_df["pace_min_per_km"], marker="o", linestyle="-")
plt.title("平均ペースの推移")
plt.xlabel("日付")
plt.ylabel("ペース (分/㎞)")
plt.gca().yaxis.set_major_formatter(FuncFormatter(mmss_formatter))
plt.grid(True)
plt.tight_layout()
pace_path = out("pace.png")
plt.savefig(pace_path)
print("保存:", pace_path)
# plt.show()
plt.close()

# ==== 3) 平均心拍数（列がある場合のみ） ====
if "平均心拍数" in plot_df.columns:
    plt.figure(figsize=(10, 5))
    plt.plot(plot_df["日付"], plot_df["平均心拍数"], marker="o", linestyle="-")
    plt.title("平均心拍数の推移")
    plt.xlabel("日付")
    plt.ylabel("心拍数 (bpm)")
    plt.grid(True)
    plt.tight_layout()
    hr_path = out("heart_rate.png")
    plt.savefig(hr_path)
    print("保存:", hr_path)
    # plt.show()
    plt.close()
