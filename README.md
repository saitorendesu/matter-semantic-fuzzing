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
