# 📦 Sample Super XXXXX Tableau Installer

`SSX_installer_***.exe` は **My Tableau Repository** 内へ、業種別リソース（シェイプ／カラーパレット／サンプル Excel／PDF など）をワンクリックで配置するインストーラーです。  
ここでは **エンドユーザー向け手順** と **開発者向けビルド方法** を１つのドキュメントにまとめています。

---

## 1. ユーザー向けガイド (Windows / Mac)

### 1-1. ダウンロード

1. GitHub の **Actions → 最新のビルド → Artifacts** から、ご自身のOS用の `Windows-installer.zip` または `macOS-installer.zip` をダウンロード。  
2. 任意の場所（例：デスクトップ）に保存し、zipファイルを解凍。  
3. 実行ファイルが出てきたことを確認。

### 1-2. インストール手順

| # | 操作 | 説明 |
|---|------|------|
| ① | インストーラーをダブルクリック | `SSX_installer_win.exe` または `SSX_installer_mac` を起動 |
| ② | **OK** をクリック | スプラッシュ画面表示後、フォルダ選択画面が出ます |
| ③ | *My Tableau Repository* を選ぶ | 例：`C:\Users\<あなた>\Documents\My Tableau Repository` または `/Users/<あなた>/Documents/マイ Tableau リポジトリ` |
| ④ | 完了ダイアログを確認 | コピーされた項目の一覧が表示されます |

> ⚠ カスタムでMy Tableauリポジトリを移動している場合は、その移動後のフォルダを選択してください。  
> 同名ファイルがあれば上書き or バックアップ後上書きされますので、再実行しても問題ありません。

### 1-3. 配置される内容

以下のリソースが、選択したリポジトリにコピーされます：

| 配置先 | ファイル／フォルダ | 内容 |
|--------|----------------------|------|
| `Preferences.tps` | カラーパレット | マークカードの色設定に使えます。 |
| `Shapes\ssf_curry` ／ `形状\ssf_curry` | アイコン（Shapes） | マークカードの形状で使用。 |
| `Themes\ssf_curry.json` | テーマ設定ファイル | UI の色など全体のスタイルに適用可能。 |
| `Datasources\サンプルスーパーファクトリー_生産管理.xlsx`<br>`Datasources\サンプルスーパーファクトリー_製造技術.xlsx`<br>`Datasources\サンプルスーパーファクトリー_品質管理.xlsx`<br>`Datasources\サンプルsーパーファクトリー_製品マスタ.xlsx` | サンプル Excel データ群 | Tableau の “新しいデータソース” から読み込めます。 |
| `利用上の注意点.pdf` | 利用マニュアル PDF | 内容を確認できます。 |

---

## 2. 開発者向けガイド

> 動作確認環境：**Python 3.13 + PyInstaller 6.x**（Windows・macOS 双方）  
> 初回のみ `pip install pyinstaller` を実行してください。

### 2-1. フォルダ構成（例）

```text
build/
├─ ssx_installer.py
├─ Shape.zip
├─ Preferences.tps
├─ ssf_curry.json
├─ サンプルスーパーファクトリー_生産管理.xlsx
├─ サンプルスーパーファクトリー_製造技術.xlsx
├─ サンプルスーパーファクトリー_品質管理.xlsx
├─ サンプルスーパーファクトリー_製品マスタ.xlsx
├─ 利用上の注意点.pdf
└─ ssx.png
