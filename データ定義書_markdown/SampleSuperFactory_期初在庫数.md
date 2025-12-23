# 商品マスタテーブル定義書

## テーブル概要
- テーブル名: 期初在庫数  
- ファイル名:
  - SampleSuperFactory_期初在庫数.csv
  - SampleSuperFactory_生産管理.xlsx - 2._期初在庫数  
- 総レコード数: -
- 作成日: 2025/9/20
- 最終更新日: 2025/9/20


## テーブル説明
各商品の工場別期初在庫数を管理するマスタテーブル。工場×商品のマトリックス形式で在庫配置戦略を可視化し、在庫最適化・生産計画・物流戦略の基盤データを提供する。


## 利用用途
- 期初在庫状況の把握
- 工場別在庫配分戦略分析
- 商品別在庫最適化
- 地域別供給体制評価
- 在庫投資効率分析
- 物流コスト最適化


## カラム定義
| No | カラム名/日本語 | カラム名/英語 | データ型 | PK | NULL許可 | 説明 | 備考 | サンプル |
|---|---------|---------|----------|----------|---|------|------|-----|
| 1 | 商品ID | product_id | VARCHAR(3) | PK | NOT NULL | 商品識別子 | 3文字コード | DKA |
| 2 | 商品名 | product_name | VARCHAR(50) | | NOT NULL | 商品の正式名称 | カレー製品名 | だからこそカレー甘口 |
| 3 | 年月日 | inventory_date | DATE | PK | NOT NULL | 在庫基準日 | | 2023/1/1 |
| 4 | 岡山工場 | opening_inventory_okayama | INTEGER | | NOT NULL | 岡山工場の期初在庫数 | 単位: 個 | 30000 |
| 5 | 埼玉工場 | opening_inventory_saitama |INTEGER | | NOT NULL | 埼玉工場の期初在庫数 | 単位: 個 | 30000 |
| 6 | 静岡工場 | opening_inventory_shizuoka| INTEGER | | NOT NULL | 静岡工場の期初在庫数 | 単位: 個 | 30000 |
| 7 | 大阪工場 | opening_inventory_osaka | INTEGER | | NOT NULL | 大阪工場の期初在庫数 | 単位: 個 | 30000 |
| 8 | 福島工場 | opening_inventory_fukushima | INTEGER | | NOT NULL | 福島工場の期初在庫数 | 単位: 個 | 30000 |


## 制約・ルール

### 主キー
- `商品ID` + `年月日`: 商品・期の組み合わせで一意
  
### 外部キー（推定）
- `商品ID`: 商品マスタ・製品マスタテーブルとの関連


### ビジネスルール
1. データ登録タイミング
   - 期初初日に登録する
  
2. データ単位
   - 期単位での管理
   - `年月日`は毎期初初日で統一 
     - 例、2023年1期は2023/1/1

3. 在庫表記
   - 万単位で登録する
   - 在庫なしの場合は0と明示的に登録する

## DDLサンプル
```sql
-- PostgreSQL 互換 DDL サンプル: 期初在庫テーブル
CREATE TABLE opening_inventory (
   product_id VARCHAR(3) NOT NULL,
   product_name VARCHAR(50) NOT NULL,
   inventory_date DATE NOT NULL,
   opening_inventory_okayama INTEGER NOT NULL DEFAULT 0,
   opening_inventory_saitama INTEGER NOT NULL DEFAULT 0,
   opening_inventory_shizuoka INTEGER NOT NULL DEFAULT 0,
   opening_inventory_osaka INTEGER NOT NULL DEFAULT 0,
   opening_inventory_fukushima INTEGER NOT NULL DEFAULT 0,
   PRIMARY KEY (product_id, inventory_date)
);
```

## 注意事項

1. **データ形式**: CSV形式、UTF-8エンコーディング
2. **機密性**: Mid
3. **更新頻度**: 毎月初日に`生産計画数`を登録し、毎月月末に`出来高数`/`出荷実績数`を更新する
4. **アクセス制御**: 

## 更新履歴

| 日付 | バージョン | 変更内容 |
|------|-----------|----------|
| 2025/09/20 | 1.0 | 初版作成 |
