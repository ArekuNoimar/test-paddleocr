"""PaddleOCRの出力ディレクトリ内の *_res.json から 'rec_texts' を抽出し、
ファイル番号順に並べてJSON配列として標準出力します。

使い方:
  python get-texts.py --select-dir /path/to/output
"""

import os
import re
import glob
import json
import argparse

def sort_key(path):
    """
    ファイル名に含まれる番号を抽出して数値として返します。

    例: 'sample-multilingual-text_0_res.json' -> 0

    Args:
        path (str): 対象ファイルのパス。

    Returns:
        int: ソート用の数値キー。パターンに合致しない場合は 10**9 を返します。
    """
    name = os.path.basename(path)
    m = re.search(r"_(\d+)_res\.json$", name)
    return int(m.group(1)) if m else 10**9

def extract_rec_texts(data):
    """
    PaddleOCR出力JSONから 'rec_texts' を抽出します。

    入力は下記のいずれにも対応します:
      - トップレベルに 'rec_texts' を持つ dict
      - トップレベルに 'res' を持ち、その中に 'rec_texts' がある dict
      - 上記の dict の配列（list）

    Args:
        data (dict | list): JSONロード後のオブジェクト。

    Returns:
        list[str]: 'rec_texts' に含まれる文字列の一覧（存在しない場合は空リスト）。
    """
    texts = []
    if isinstance(data, dict):
        if isinstance(data.get("rec_texts"), list):
            texts.extend(data["rec_texts"])
        elif isinstance(data.get("res"), dict) and isinstance(data["res"].get("rec_texts"), list):
            texts.extend(data["res"]["rec_texts"])
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if isinstance(item.get("rec_texts"), list):
                    texts.extend(item["rec_texts"])
                elif isinstance(item.get("res"), dict) and isinstance(item["res"].get("rec_texts"), list):
                    texts.extend(item["res"]["rec_texts"])
    return texts

def main():
    """
    コマンドライン引数を解析し、--select-dir にある *_res.json を番号順に処理して
    'rec_texts' を収集し、番号順の配列をJSONで標準出力します。

    必須:
        --select-dir: *_res.json が存在するディレクトリ。

    Raises:
        SystemExit: 指定ディレクトリが存在しない、または該当JSONが見つからない場合。

    実行例:
        python get-texts.py --select-dir /home/ubuntu/python_project/test-paddleocr/src/output
    """
    parser = argparse.ArgumentParser(description="PaddleOCRの出力JSONからrec_textsを抽出して番号順に出力")
    parser.add_argument("--select-dir", required=True, help="*_res.json が存在するディレクトリを指定")
    args = parser.parse_args()

    output_dir = args.select_dir
    if not os.path.isdir(output_dir):
        raise SystemExit(f"--select-dir のディレクトリが見つかりません: {output_dir}")

    json_files = sorted(glob.glob(os.path.join(output_dir, "*_res.json")), key=sort_key)
    if not json_files:
        raise SystemExit(f"{output_dir} に *_res.json が見つかりません")

    results = []
    for jf in json_files:
        name = os.path.basename(jf)
        m = re.search(r"_(\d+)_res\.json$", name)
        if not m:
            continue
        idx = int(m.group(1))
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)
        texts = extract_rec_texts(data)
        results.append({
            "index": idx,
            "file": name,
            "rec_texts": texts
        })

    print(json.dumps(results, ensure_ascii=False))

if __name__ == "__main__":
    main()