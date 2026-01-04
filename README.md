# Matter Semantic Fuzzing using LLM

大規模言語モデル（LLM）を活用して、スマートホーム規格「Matter」の実装バグ（論理的脆弱性）を検知するファジングシステムです。
Raspberry Piを用いた実機検証環境において、仕様書に基づいた意味論的（Semantic）な攻撃を行います。

![System Diagram](images/system_diagram.png)

## 📌 Features
* **LLM-Driven:** Gemini 3 Pro を用いて仕様書から「意味のある異常値」を自動抽出
* **Semantic Fuzzing:** 単なるビット反転ではなく、論理バグ（仕様違反）を狙い撃ち
* **Physical Feedback:** 脆弱性検知時にGPIO経由でLEDを点灯させ、物理的に通知

## 📂 Repository Structure

```text
.
├── src/
│   ├── matter_fuzzer_ultimate.py  # 攻撃実行用スクリプト (Main Fuzzer)
│   └── gpio_server.py             # ラズパイ側で動くLED制御サーバ
├── docs/
│   ├── 学校提出用論文.doc
│   └── 開発者向け文書.docx        # 詳細なセットアップ手順書
└── images/
    ├── system_diagram.png         # システム構成図
    └── wiring_photo.jpg           # 配線写真
🛠️ System Requirements
Tester (Attacker)
Hardware: MacBook Pro (Apple Silicon M1/M2/M3 Recommended)

Software:

Python 3.9+

Matter SDK (chip-tool) environment

Network: Ethernet (IPv6) connected to DUT

DUT (Victim)
Hardware: Raspberry Pi 4 Model B (4GB RAM+)

OS: Ubuntu Core 22 (Server)

Application: Matter Linux Lighting App

Peripherals:

LED Indicator (GPIO 21 / Pin 40)

Resistor (330Ω)

🚀 Quick Start
1. DUT (Raspberry Pi) Setup
ラズパイにSSH接続し、異常検知用のLEDサーバとMatterアプリを起動します。

Bash

# 1. SSH接続
ssh ubuntu@ubuntu.local

# 2. LEDサーバの起動 (バックグラウンド実行)
sudo python3 ~/src/gpio_server.py &

# 3. Matter Lighting Appの起動
cd ~/matter/connectedhomeip
sudo ./out/lighting-app/chip-lighting-app
2. Tester (Mac) Setup & Attack
Mac側で攻撃スクリプトを実行します。

Bash

# 1. スクリプトのあるディレクトリへ移動
cd src

# 2. 攻撃スクリプトの実行
# (環境に合わせて matter_fuzzer_ultimate.py 内のパス設定を確認してください)
python3 matter_fuzzer_ultimate.py
📊 Evaluation
実験結果の詳細は docs/学校提出用論文.doc を参照してください。 本ツールを用いて、タイミング依存の論理バグ（Timing-dependent Logic Bug） を検知することに成功しました。

📜 License
This project is for academic research purposes.

👥 Author
Ren Saito (Matsuzaki Lab, Chuo University)
