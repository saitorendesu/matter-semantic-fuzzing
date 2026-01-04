# Matter Semantic Fuzzing using LLM

大規模言語モデル（LLM）を活用して、スマートホーム規格「Matter」の実装バグ（論理的脆弱性）を検知するファジングシステムです。
Raspberry Piを用いた実機検証環境において、仕様書に基づいた意味論的（Semantic）な攻撃を行います。

## リポジトリ構成
* `src/`: 攻撃用Pythonスクリプト (`matter_fuzzer_ultimate.py`) および GPIO制御サーバ (`gpio_server.py`)
* `docs/`: 論文および開発者向けドキュメント
* `images/`: 実験環境の構成図や配線写真

## システム要件
* **Tester:** MacBook Pro (macOS) / chip-tool
* **DUT:** Raspberry Pi 4 / Matter Linux Lighting App
* **LLM:** Gemini 3 Pro (Test case generation)

## 使い方
詳細は `docs/開発者向け文書.docx` を参照してください。

## Author
Ren Saito (Matsuzaki Lab, Chuo University)
