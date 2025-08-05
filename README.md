# 📦 Sample Super xxx Tableau Installer

`SSX_installer_***.exe` は **My Tableau Repository** 内へ業種別リソース（シェイプ／カラーパレット／サンプル Excel など）をワンクリックで配置するインストーラーです。ここでは **エンドユーザー向け手順** と **開発者向けビルド方法** を１つのドキュメントにまとめています。

---

## 1.ユーザー向けガイド( Windows / Mac )

### 1-1. ダウンロード
1. GitHub の **Actions --> Update build-installers.yml の最新版を開く --> Artifacts** からお使いのOSに合わせて、最新のWindows-installer.zip、もしくは、macOS-installer.zip　をダウンロード。
2. お使いのパソコンの任意の場所（デスクトップ等）に保存してzipファイルを解凍。
3. ssx_installer_*.exe が出てきたことを確認。

### 1-2. インストール手順

| 手順 | 操作 | 画面例 |
|------|------|--------|
| ① | `SSX_installer_win.exe` もしくは `SSX_installer_mac.exe` をダブルクリック | スプラッシュが表示 |
| ② | **OK** をクリック | フォルダー選択ダイアログ |
| ③ | *My Tableau Repository* を選択 | 例: `C:\Users\<あなた>\Documents\My Tableau Repository` |
| ④ | 「インストール完了！」ダイアログ | 処理終了 |

> カスタム位置にリポジトリを移動している場合は、そのフォルダを選択してください。  
> **再実行しても OK** – 同名フォルダは自動バックアップ後に上書きされます。

### 1-3. 配置される内容

| 配置先 | 追加ファイル／フォルダ |利用方法|
|--------|-----------------------|------------------------|
| `Preferences.tps` | カラーパレット |マークカードの色から選択できます。|
| `Shapes\ssf_curry` / `形状\ssf_curry` | 製造業向けアイコン |マークカードの形状から選択できます。|
| `Themes\ssf_curry.json` | カスタムテーマ |メニューの書式設定→カスタムテーマのインポート→jsonを選択すると適用されます。|
| `Datasources\サンプルスーパーファクトリー.xlsx`<br>`データソース\...` | サンプル Excel データ |

アンインストールは該当フォルダ、ファイルを手動削除して下さい。

---

## 2. 開発者向けガイド

> 動作確認環境：**Python 3.13 + PyInstaller 6.x**（Windows 11）  
> 初回のみ `pip install pyinstaller` を実行してください。

### 2-1. フォルダ構成（例）

- **build/**  ← ビルド用作業ディレクトリ  
  - `ssx_installer.py` … メインスクリプト  
  - `Shape.zip` … `Shapes/<業種フォルダ>/…` をまとめた ZIP  
  - `Preferences.tps` … Tableau 用カラーパレット  
  - `ssf_curry.json` … JSON パレット例  
  - `サンプルスーパーファクトリー.xlsx` … サンプルデータ  
  - `ssx.png` … スプラッシュ画像

### 2-2. ビルド（1 行コマンド）

1. コマンドプロンプト / PowerShell で **build フォルダに移動**  
2. 下記 1 行をコピーして実行

```cmd
py -3.13 -m PyInstaller --clean --onefile --noconsole --add-data "Shape.zip;." --add-data "ssf_curry.json;." --add-data "サンプルスーパーファクトリー.xlsx;." --add-data "Preferences.tps;." --add-data "ssx.png;." ssx_installer.py
