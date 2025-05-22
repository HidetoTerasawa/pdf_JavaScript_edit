このコードは、**PDFファイルに埋め込まれたJavaScriptを確認・追加・削除できるPythonスクリプト**です。  
`pypdf`ライブラリを使ってPDFの内部構造を操作しています。

---

### 主な機能

1. **check**  
   PDF内に埋め込まれているJavaScriptを一覧表示します。

2. **add**  
   指定したJavaScriptコードをPDFに埋め込みます。

3. **remove**  
   PDF内の「/Names」→「/JavaScript」エントリ（自動実行などのJavaScript）を削除します。

---

### 使い方例

- JavaScriptの確認  
  ```
  python "import sys.py" check input.pdf
  ```

- JavaScriptの追加  
  ```
  python "import sys.py" add input.pdf --output output.pdf --js "app.alert('Hello!');"
  ```

- JavaScriptの削除  
  ```
  python "import sys.py" remove input.pdf --output output.pdf
  ```

---

### 補足

- 削除機能は「/Names」→「/JavaScript」配下のスクリプトのみを消します。  
  ページやフォームに直接埋め込まれたスクリプトは対象外です。
- 主に「PDFを開いたときに自動実行されるJavaScript」や「警告の原因」を除去できます。

---

**PDFのセキュリティや動作確認に便利なツールです。**
