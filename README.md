```markdown
# 📦 Sample Super xxx Tableau Installer

`ssx_installer.exe` は **My Tableau Repository** 内へ  
業種別リソース（シェイプ／カラーパレット／サンプル Excel など）を
ワンクリックで配置するインストーラーです。  
ここでは **エンドユーザー向け手順** と **開発者向けビルド方法** を
１つのドキュメントにまとめています。

---

## 1. Windowsユーザー向けガイド

### 1-1. ダウンロード
1. GitHub の **Releases** から `ssx_installer.exe` を取得  
2. 好きな場所（デスクトップ等）に保存

### 1-2. インストール手順

| 手順 | 操作 | 画面例 |
|------|------|--------|
| ① | `ssx_installer.exe` をダブルクリック | スプラッシュが表示 |
| ② | **OK** をクリック | フォルダー選択ダイアログ |
| ③ | *My Tableau Repository* を選択 | 例: `C:\Users\<あなた>\Documents\My Tableau Repository` |
| ④ | 「インストール完了！」ダイアログ | 処理終了 |

> カスタム位置にリポジトリを移動している場合は、そのフォルダを選択してください。  
> **再実行しても OK** – 同名フォルダは自動バックアップ後に上書きされます。

### 1-3. 配置される内容

| 配置先 | 追加ファイル／フォルダ |
|--------|-----------------------|
| `Shapes\ssf_curry` / `形状\ssf_curry` | 製造業向けアイコン |
| `Shapes\ssb_togin` など | 金融業向けアイコン ほか |
| `Themes\ssf_curry.json` | カラーパレット |
| `Datasources\サンプルスーパーファクトリー.xlsx`<br>`データソース\...` | サンプル Excel データ |

アンインストールは該当フォルダを手動削除するだけです。

---

## 2. 開発者向けガイド

> 動作確認環境：**Python 3.13 + PyInstaller 6.x**（Windows 11）  
> 初回のみ `pip install pyinstaller` を実行してください。

### 2-1. フォルダ構成（例）

```

build/                       ← ビルド用作業ディレクトリ
│  ssx\_installer.py          ← 本スクリプト
│  Shape.zip                 ← Shapes/<業種>/画像.png …
│  Preferences.tps
│  ssf\_curry.json
│  サンプルスーパーファクトリー.xlsx
│  ssx.png                   ← スプラッシュ画像

````

### 2-2. ビルド（1 行コマンド）

```cmd
py -3.13 -m PyInstaller --clean --onefile --noconsole ^
  --add-data "Shape.zip;." ^
  --add-data "ssf_curry.json;." ^
  --add-data "サンプルスーパーファクトリー.xlsx;." ^
  --add-data "Preferences.tps;." ^
  --add-data "ssx.png;." ^
  ssx_installer.py
````

| オプション         | 意味                         |
| ------------- | -------------------------- |
| `--onefile`   | 単一 EXE 化                   |
| `--noconsole` | GUI 専用（デバッグ時は `--console`） |
| `--add-data`  | 付属リソースを同梱                  |

生成物は `dist\ssx_installer.exe` に出力されます。

### 2-3. カスタマイズ

| 変更内容          | 手順                                                    |
| ------------- | ----------------------------------------------------- |
| 業種フォルダの追加     | `Shape.zip` に `Shapes/<新フォルダ>/…` を追加                  |
| カラーパレット追加     | `Themes/<新>.json` を置き、`install()` に `cp_retry()` 行を追記 |
| サンプル Excel 追加 | ファイルを配置し、`install()` の Datasources ループへ追記             |
| スプラッシュ変更      | `ssx.png` を差し替え（推奨 960 × 540 以内 PNG）                  |

### 2-4. トラブルシューティング

| 症状                | 対処法                                    |
| ----------------- | -------------------------------------- |
| EXE が無反応          | `--console` でビルドし、コンソールログを確認           |
| リポジトリ自動検出不可       | ユーザーに手動でフォルダを指定してもらう                   |
| `PermissionError` | Tableau/Explorer でフォルダを開いたままになっていないか確認 |

---

## 3. ライセンス

本リポジトリは **MIT License** です。詳細は [`LICENSE`](LICENSE) を参照してください。

```

> **使い方**  
> 1. 上記内容を `README.md` に保存してコミット  
> 2. 必要に応じてスクリーンショットや GIF を追加し、リンクを貼る  
> 3. `dist\ssx_installer.exe` を Release に添付して配布  
> これで利用者・開発者の両方が 1 ファイルで済み、管理も簡単です。
```
