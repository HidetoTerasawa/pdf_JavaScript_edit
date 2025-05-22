import sys
import argparse
from pypdf import PdfReader, PdfWriter

def check_javascript(pdf_path):
    reader = PdfReader(pdf_path)
    js_list = []
    root = reader.trailer["/Root"]
    if "/Names" in root:
        names = root["/Names"]
        if "/JavaScript" in names:
            js_names = names["/JavaScript"]["/Names"]
            for i in range(1, len(js_names), 2):
                js = js_names[i].get_object()
                js_list.append(js["/JS"])
    if js_list:
        print("埋め込まれているJavaScript:")
        for idx, js in enumerate(js_list, 1):
            print(f"[{idx}] {js}")
    else:
        print("JavaScriptは埋め込まれていません。")

def add_javascript(pdf_path, output_path, js_code):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_js(js_code)
    with open(output_path, "wb") as f:
        writer.write(f)
    print("JavaScriptを追加しました。")

def remove_javascript(pdf_path, output_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    # ページをすべて追加
    for page in reader.pages:
        writer.add_page(page)
    # /Namesから/JavaScriptだけを除去
    root = reader.trailer["/Root"]
    if "/Names" in root:
        names = root["/Names"]
        if "/JavaScript" in names:
            del names["/JavaScript"]
        # /Namesが空なら削除
        if len(names.keys()) == 0:
            del root["/Names"]
    # メタデータをコピー
    if "/Info" in reader.trailer:
        writer.add_metadata(reader.metadata)
    # カタログの/Namesを上書き
    if "/Names" in root:
        writer._root_object.update({"/Names": root["/Names"]})
    with open(output_path, "wb") as f:
        writer.write(f)
    print("JavaScriptを削除しました。")

def main():
    parser = argparse.ArgumentParser(description="PDFのJavaScript操作ツール")
    parser.add_argument("mode", choices=["check", "add", "remove"], help="操作モード")
    parser.add_argument("pdf_path", help="PDFファイルのパス")
    parser.add_argument("--output", help="出力ファイル名（add/remove時必須）")
    parser.add_argument("--js", help="追加するJavaScriptコード（add時必須）")
    args = parser.parse_args()

    if args.mode == "check":
        check_javascript(args.pdf_path)
    elif args.mode == "add":
        if not args.output or not args.js:
            print("addモードでは--outputと--jsが必要です。")
            sys.exit(1)
        add_javascript(args.pdf_path, args.output, args.js)
    elif args.mode == "remove":
        if not args.output:
            print("removeモードでは--outputが必要です。")
            sys.exit(1)
        remove_javascript(args.pdf_path, args.output)

if __name__ == "__main__":
    main()



"""🔴このコードはpython "import sys.py" remove input.pdf --output output.pdfを実行することで、何のJavaScriptを消してるの？


このコードは
```python
python "import sys.py" remove input.pdf --output output.pdf
```
を実行すると、**PDF内の「/Names」辞書の中にある「/JavaScript」エントリ**を削除します。

つまり、
- PDFのカタログ（/Root）の「/Names」→「/JavaScript」に登録されている**全てのJavaScriptアクション**（自動実行やボタンアクションなど）
を削除します。

**ページ内に直接埋め込まれているスクリプトや、AcroFormのアクションなどは消しませんが、
「他のパソコンで開いたときに警告が出る」主な原因である「/Names」→「/JavaScript」部分を消します。**

---

### まとめ
- 消しているのは「/Names」→「/JavaScript」配下のJavaScriptです。
- これにより、PDFを開いたときのJavaScript自動実行や警告の主な原因が除去されます。

"""
"""🔴コマンド例
JavaScript確認:
python "import sys.py" check input.pdf
JavaScript追加:
python "import sys.py" add input.pdf --output output.pdf --js "app.alert('Hello!');"
JavaScript削除:
python "import sys.py" remove input.pdf --output output.pdf
"""
