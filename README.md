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

