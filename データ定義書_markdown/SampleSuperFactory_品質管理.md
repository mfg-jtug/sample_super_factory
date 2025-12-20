# 品質管理テーブル定義書

## テーブル概要
- テーブル名: 品質管理  
- ファイル名:
  - SampleSuperFactory_品質管理.csv
  - SampleSuperFactory_品質管理.xlsx - inspection_result_all_machines
- 総レコード数: 396,002
- 作成日: 2025/12/8
- 最終更新日: 2025/12/8


## テーブル説明
製造ラインでの各商品の製造時の品質検査結果を記録するトランザクションテーブル。製造時刻、QRコード、ロット情報、充填・シーリング工程のパラメータ、重量測定値、不良情報などを一元管理し、品質保証・トレーサビリティ・工程改善の基盤データを提供する。


## 利用用途
- 製造品質のリアルタイム監視
- 不良品の原因分析・傾向分析
- ロットトレーサビリティ管理
- 製造工程パラメータの最適化
- 重量管理と規格適合性の確認
- 製造ラインごとの品質比較分析


## Column Definitions
| No | Field Name_Jp | Field Name_Eng | Data Type | PK | NULL | Description | Notes | Sample |
|---|---------|---------|----------|----------|---|------|------|-----|
| 1 | 行ID | row_id | INTEGER | PK | NOT NULL | Unique identifier for inspection record | 連番 | 1 |
| 2 | 検査時刻 | inspection_datetime | TIMESTAMP | | NOT NULL | Quality inspection date and time | YYYY/MM/DD HH:MM:SS形式 | 2025/7/1 10:16:00 |
| 3 | 製造ライン | production_line | VARCHAR(1) | | NOT NULL | Production line identifier | A, B, C等 | A |
| 4 | QRコード | qr_code | VARCHAR(7) | | NOT NULL | Individual product identification QR code | 製造ライン+6桁英数字 | A000001 |
| 5 | 商品ID | product_id | VARCHAR(3) | | NOT NULL | Product identifier | 3文字コード | KMC |
| 6 | ロットID | lot_id | VARCHAR(15) | | NOT NULL | Manufacturing lot identifier | B+YYYYMMDD+製造ライン+ロット番号 | B2025070101A200 |
| 7 | NGカテゴリ | ng_category | VARCHAR(50) | | NULL | Major defect category | 不良発生時のみ記録 | |
| 8 | NGサブカテゴリ | ng_subcategory | VARCHAR(50) | | NULL | Detailed defect subcategory | 不良発生時のみ記録 | |
| 9 | 充填圧力 | filling_pressure | DECIMAL(10,2) | | NOT NULL | Filling process pressure | 単位: Pa | 232.75 |
| 10 | 充填速度 | filling_speed | DECIMAL(10,3) | | NOT NULL | Filling process speed | 単位: mm/sec | 6.18 |
| 11 | 充填量 | filling_weight | DECIMAL(10,2) | | NOT NULL | Weight of filled contents | 単位: g | 200.87 |
| 12 | 重量上限 | weight_upper_limit | INTEGER | | NOT NULL | Upper weight limit | 単位: g | 210 |
| 13 | 重量下限 | weight_lower_limit | INTEGER | | NOT NULL | Lower weight limit | 単位: g | 194 |
| 14 | シーリング温度 | sealing_temp | DECIMAL(10,2) | | NOT NULL | Sealing process temperature | 単位: ℃ | 199.21 |
| 15 | シーリング圧力 | sealing_pressure | DECIMAL(10,3) | | NOT NULL | Sealing process pressure | 単位: MPa | 0.963 |


## 制約・ルール

### 主キー
- `行ID`: 各検査記録に対する一意の連番
  
### 外部キー（推定）
- `商品ID`: 商品マスタテーブルとの関連
- `製造ライン`: 製造ラインマスタテーブルとの関連
- `ロットID`: ロット管理テーブルとの関連


### ビジネスルール
1. データ登録タイミング
   - 製造ライン上で製品が検査工程を通過する都度記録
  
2. 品質判定基準
   - 重量判定: `重量下限[g]` ≤ `充填量[g]` ≤ `重量上限[g]`
   - 不良品の場合は`NGカテゴリ`と`NGサブカテゴリ`に分類内容を記録
   - 良品の場合は`NGカテゴリ`と`NGサブカテゴリ`は空欄

3. QRコード・ロットID
   - `QRコード`: 個品レベルのトレーサビリティを実現
   - `ロットID`: 製造日・ライン・ロット番号から構成される一括管理単位
   
4. 工程パラメータ
   - 充填工程: 圧力・速度・重量の3指標で管理
   - シーリング工程: 温度・圧力の2指標で管理
   - これらのパラメータは製造標準に基づいて設定・監視される

## DDLサンプル
```sql
-- PostgreSQL 互換 DDL サンプル: 品質管理テーブル
CREATE TABLE quality_control (
   row_id INTEGER PRIMARY KEY,
   inspection_time TIMESTAMP NOT NULL,
   production_line VARCHAR(1) NOT NULL,
   qr_code VARCHAR(7) NOT NULL,
   product_id VARCHAR(3) NOT NULL,
   lot_id VARCHAR(15) NOT NULL,
   ng_category VARCHAR(50),
   ng_subcategory VARCHAR(50),
   filling_pressure_pa DECIMAL(10,2) NOT NULL,
   filling_speed_mm_sec DECIMAL(10,3) NOT NULL,
   filling_weight_g DECIMAL(10,2) NOT NULL,
   weight_upper_limit_g INTEGER NOT NULL,
   weight_lower_limit_g INTEGER NOT NULL,
   sealing_temperature_c DECIMAL(10,2) NOT NULL,
   sealing_pressure_mpa DECIMAL(10,3) NOT NULL
);
```

## 注意事項

1. **データ形式**: CSV形式、UTF-8エンコーディング
2. **機密性**: High（個品トレーサビリティ情報を含む）
3. **更新頻度**: リアルタイム（製造ライン上で検査実施時に随時追加）
4. **アクセス制御**: 品質管理部門、製造部門の参照権限が必要

## 更新履歴

| 日付 | バージョン | 変更内容 |
|------|-----------|----------|
| 2025/12/08 | 1.0 | 初版作成 |
