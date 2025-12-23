# 工場マスタテーブル定義書

## テーブル概要
- テーブル名: 工場マスタ
- ファイル名:
  - SampleSuperFactory_工場マスタ.csv
  - SampleSuperFactory_生産管理.xlsx - 8.工場マスタ
- 総レコード数: 5
- 作成日: 2025/9/20
- 最終更新日: 2025/9/20


## テーブル説明
カレー製造を行う全工場の基本情報と生産能力を管理するマスタテーブル。各工場の生産効率、設備仕様、稼働体制を定義する。


## 利用用途
- 設備投資計画策定
- 生産計画精度向上
- 工場別パフォーマンス分析
- 需要予測精度向上


## カラム定義
| No | カラム名/日本語 | カラム名/英語 | データ型 | PK | NULL許可 | 説明 | 備考 | サンプル |
|---|---------|---------|----------|----------|---|------|------|-----|
| 1 | 工場名 | factory_name | VARCHAR(10) | PK | NOT NULL | 工場の正式名称 |  | 大阪 |
| 2 | パックByLOT | quantity_per_lot | INTEGER | | NOT NULL | 1ロット当たりの包装数 | 単位: 個/ロット | 5000 |
| 3 | 時間ByLOT | hours_per_lot | DECIMAL(3,1) | | NOT NULL | 1ロット製造に要する時間 | 単位: 時間/ロット | 6 |
| 4 | 稼働時間By日 | hours_per_day | DECIMAL(3,1) | | NOT NULL | 1日当たりの稼働時間 | 単位: 時間 | 12 |
| 5 | LOTBy日 | lots_per_day | DECIMAL(3,1) | | NOT NULL | 1日当たりの最大ロット数 | 単位: ロット/日 | 2 |
| 6 | 工場設立 | established_year | INTEGER | | | 工場の設立年 | 西暦年 | 2019 |


## 制約・ルール

### 主キー
- `工場名`: 工場名で一意

### 外部キー（推定）


### ビジネスルール

1. データ登録タイミング
   - 工場の新設や設備拡張時に随時更新する

2. データ単位
   - 工場単位での管理


## DDLサンプル
```sql
-- PostgreSQL 互換 DDL サンプル: 工場マスタ
CREATE TABLE factory_master (
   factory_name VARCHAR(50) PRIMARY KEY,
   quantity_per_lot INTEGER NOT NULL,                         -- 1ロット当たりの包装数（個/ロット）
   hours_per_lot DECIMAL(3,1) NOT NULL,                       -- 1ロット製造に要する時間（時間/ロット）
   hours_per_day DECIMAL(3,1) NOT NULL,                       -- 1日当たりの稼働時間（時間）
   lots_per_day DECIMAL(3,1) NOT NULL,                        -- 1日当たりの最大ロット数（ロット/日）
   established_year INTEGER
);
```


## 注意事項

1. **データ形式**: CSV形式、UTF-8エンコーディング
2. **機密性**: High/各工場の生産効率に関するデータの為
3. **更新頻度**: 工場の新設や設備拡張時に随時更新する
4. **アクセス制御**: 

## 更新履歴

| 日付 | バージョン | 変更内容 |
|------|-----------|----------|
| 2025/09/20 | 1.0 | 初版作成 |
