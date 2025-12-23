# 商品マスタテーブル定義書

## テーブル概要
- テーブル名: 商品マスタ  
- ファイル名:
  - SampleSuperFactory_商品マスタ.csv
  - SampleSuperFactory_商品マスタ.xlsx - 商品マスタ
- 総レコード数: 20行
- 作成日: 2025/9/20
- 最終更新日: 2025/9/20


## テーブル説明
カレー商品の販売・在庫・価格に関する基本情報を管理するマスタテーブル。商品の市場戦略、在庫管理、収益性分析の基盤データを提供する。


## 利用用途
- 商品カタログ管理
- 価格戦略立案
- 在庫最適化
- 収益性分析
- 販売戦略策定
- 原価管理
- マーケティング戦略


## カラム定義
| No | カラム名/日本語 | カラム名/英語 | データ型 | PK | NULL許可 | 説明 | 備考 | サンプル |
|---|---------|---------|----------|----------|---|------|------|-----|
| 1 | 商品名 | product_name | VARCHAR(100) | | NOT NULL | 商品の正式名称 | カレー製品の商品名 | りんご＆ハチミツカレー |
| 2 | 商品ID | product_id | VARCHAR(3) | PK | NOT NULL | 商品識別子 | 3文字コード | RHC |
| 3 | 辛さ | spicy_level | VARCHAR(10) | | NOT NULL | 辛さレベル | 3段階 | 辛口 |
| 4 | カテゴリ | product_category | VARCHAR(20) | | NOT NULL | 商品のカテゴリ分類 | 7種類 | スタンダード |
| 5 | 販売単位 | sales_unit_quantity | INTEGER | | NOT NULL | 最小販売単位数量 | 単位: 個　| 1000 |
| 6 | 当期末目標在庫 | target_ending_inventory | INTEGER | | NOT NULL | 期末時点の目標在庫数<br>計画値の為、実際在庫とは異なる| 単位: 個 | 500000 |
| 7 | 販売単価 | sales_price | INTEGER | | NOT NULL | 商品の販売価格 | 単位: 円 | 340 |
| 8 | 原価率(%) | cost_percentage | DECIMAL(5,2) | | NOT NULL | 原価率(小数) | 単位: % | 80.00 |
| 9 | 内容量(g) | content_weight_gram | DECIMAL(5,2) | | NOT NULL | 内容量(小数) | 単位: g | 200.00 |
| 10 | キャッチコピー | product_catchphrase | VARCHAR(100) | | NOT NULL | 商品のキャッチコピー |  | これぞ日本の心 |
| 11 | イメージ | product_image | VARCHAR(200) | | NOT NULL | 商品のイメージ画像 | ハイパーリンク | https://drive.google.com/file/d/ssf |



## 制約・ルール

### 主キー
- `商品ID`/`product_id`: ビジネス上の一意識別子（3文字コード）


### ビジネスルール

1. **販売単位体系**
   - 2パターンの販売単位を設定
     - 大ロット商品: 主力商品群、販売単位10,000個
     - 小ロット商品: 限定・特殊商品群、販売単位1,000個

2. **在庫戦略**
   - 目標在庫は販売予測と生産効率を考慮
   - 高回転商品：高い目標在庫設定、100,000以上
   - 特殊商品：低い目標在庫設定、100,000未満

3. **販売単価計算**
   - 原価率 = 原価/販売単価


4. **価格戦略**
   1. 販売単価戦略
   - 商品ターゲットより3つの層に分類し、販売単価を設定する。
      - プレミアム帯: 500円以上
      - ミドル帯: 300-500円
      - エントリー帯: 300円未満

   1. 原価率戦略
   - 商品ターゲットより3パターンに分類し原価率を設定する
     - 高効率商品群: 60-75%
     - 標準商品群: 75-85%
     - 戦略的商品群: 85-95%


## DDLサンプル
```sql
CREATE TABLE product_master (
   product_id VARCHAR(3) PRIMARY KEY,
   product_name VARCHAR(100) NOT NULL,
   spicy_level VARCHAR(10) NOT NULL,
   product_category VARCHAR(20) NOT NULL,
   sales_unit_quantity INTEGER NOT NULL,
   target_ending_inventory INTEGER NOT NULL,
   sales_price INTEGER NOT NULL,
   cost_percentage DECIMAL(5,2) NOT NULL CHECK (cost_percentage >= 0),
   content_weight_gram DECIMAL(5,2) NOT NULL CHECK (content_weight_gram >= 0),
   product_catchphrase VARCHAR(100) NOT NULL,
   product_image VARCHAR(200) NOT NULL
);
```


## 注意事項

1. **データ形式**: CSV形式、UTF-8エンコーディング
2. **機密性**: High/機密性の高い競争情報に関するデータ
3. **更新頻度**: 商品戦略変更時に随時更新
4. **アクセス制御**: 販売・財務情報のため適切な権限管理要

## 更新履歴

| 日付 | バージョン | 変更内容 |
|------|-----------|----------|
| 2025/09/20 | 1.0 | 初版作成 |
