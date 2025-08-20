# このリポジトリについて

このリポジトリはPaddleOCRの実験用です。GPUは利用せず、CPUのみで実行します。

## 構成

```bash
test-paddleocr/
├── README.md
├── pyproject.toml
├── src
│   ├── get-texts.py
│   ├── media                                  # ドキュメント保存用ディレクトリ
│   │   └── sample-multilingual-text.pdf      # OCR実行テスト用のPDF
│   └── output                                 # OCR結果保存用ディレクトリ
└── uv.lock
```

## ライブラリ

paddleocr==3.1.1  
paddlepaddle==3.1.0  
setuptools==80.9.0  


## 初期設定

```bash
# ディレクトリ変更
cd test-paddleocr

# python 3.12.3の仮想環境を作成する
uv venv --python 3.12.3

# 仮想環境の有効化
source .venv/bin/activate

# 環境同期
uv sync
```

## 使い方

```bash
# PaddleOCRで指定ファイルをOCRし、結果を任意ディレクトリに保存
uv run paddleocr ocr -i 'DOCUMENT-FILE-PATH' --save_path 'OCR-RESULT-DIRECTORY-PATH'

# OCRしたドキュメントのindex番号, 出力ファイル名, テキスト情報を任意ディレクトリから取得
uv run python src/get-texts.py --select-dir 'OCR-RESULT-DIRECTORY-PATH'
```

## 利用例

```bash
# PaddleOCRで'src/media/sample-multilingual-text.pdf'をOCRし、結果を'src/output/sample-multilingual-text-output'に保存
uv run paddleocr ocr -i src/media/sample-multilingual-text.pdf --save_path src/output/sample-multilingual-text-output

# OCRしたドキュメントのindex番号, 出力ファイル名, テキスト情報を'src/output/sample-multilingual-text-output' から取得
uv run python src/get-texts.py --select-dir src/output/sample-multilingual-text-output
```

## 参考
[PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
