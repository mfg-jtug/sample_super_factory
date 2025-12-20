# 製造技術テーブル定義書

## テーブル概要
- テーブル名: 製造技術  
- ファイル名:
  - SampleSuperFactory_製造技術.csv
  - SampleSuperFactory_製造技術.xlsx - 製造技術
- 総レコード数: 2,925
- 作成日: 2025/12/20
- 最終更新日: 2025/12/20


## テーブル説明
製造工程における技術的パラメータと環境条件を時系列で記録するトランザクションテーブル。材料仕込み、加熱調理、冷却などの各工程における温度、圧力、環境条件を1分単位で記録し、製造品質の安定化、工程分析、トレーサビリティの基盤データを提供する。


## 利用用途
- 製造工程のリアルタイム監視
- 工程パラメータの最適化分析
- ロット別製造条件の記録・追跡
- 品質異常時の製造条件確認
- 環境条件と品質の相関分析
- 製造標準の改善・検証


## Column Definitions
| No | Field Name_Jp | Field Name_Eng | Data Type | PK | NULL | Description | Notes | Sample |
|---|---------|---------|----------|----------|---|------|------|-----|
| 1 | 測定日時 | measurement_datetime | TIMESTAMP | PK | NOT NULL | 測定日時 | YYYY/MM/DD HH:MM:SS形式、1分単位 | 2025/1/6 6:00 |
| 2 | ロットID | lot_id | VARCHAR(18) | PK | NOT NULL | ロット番号 | 商品ID+YYYYMMDD+製造回+製造ライン+ロット番号 | KMC2025010601A200 |
| 3 | 工程 | process_name | VARCHAR(20) | | NOT NULL | 工程名 | 材料仕込み、加熱調理、冷却等 | 材料仕込み |
| 4 | 工程詳細 | process_name_detail | VARCHAR(50) | | | 工程の詳細 | 各工程の詳細ステップ、NULLの場合がある | 仕込み開始 |
| 5 | ジャケット温度 | jacket_temp | DECIMAL(10,1) | | NOT NULL | ジャケット温度 | 単位: ℃ | 5.2 |
| 6 | 内容物温度 | content_temp | DECIMAL(10,1) | | NULL | 内容物の温度 | 単位: ℃、測定開始後に記録 | 6.7 |
| 7 | ジャケット圧 | jacket_pressure | DECIMAL(10,3) | | NOT NULL | ジャケット圧力 | 単位: MPa | -0.007 |
| 8 | 外気温 | room_temp | DECIMAL(10,1) | | NOT NULL | 工場内の気温 | 単位: ℃ | 5.0 |
| 9 | 湿度 | room_humidity | DECIMAL(10,1) | | NOT NULL | 工場内の湿度 | 単位: % | 39.7 |


## 制約・ルール

### 主キー
- `測定日時` + `ロットID`: 測定時刻とロットの組み合わせで一意
  
### 外部キー（推定）
- `ロットID`: ロット管理テーブルとの関連（先頭3文字が商品ID）
- `工程`: 工程マスタテーブルとの関連


### ビジネスルール
1. データ登録タイミング
   - 製造工程中、1分間隔で自動測定・記録
   - 各工程の開始から完了まで連続して記録
  
2. 工程フロー
   - 材料仕込み → 加熱調理 → 冷却 → 充填・包装の順で進行
   - 各工程には複数の詳細ステップが存在

3. 測定項目
   - `ジャケット温度`: 加熱・冷却ジャケットの温度
   - `内容物温度`: カレールーなど内容物の実測温度（工程開始後に測定可能）
   - `ジャケット圧`: ジャケット内の圧力（負圧含む）
   - `外気温`、`湿度`: 製造環境の条件
   
4. データの連続性
   - 1ロットの製造期間中、連続してデータが記録される
   - 欠測がある場合は設備異常や工程停止を示唆

## DDLサンプル
```sql
-- PostgreSQL 互換 DDL サンプル: 製造技術テーブル
CREATE TABLE process_data (
   measurement_datetime TIMESTAMP NOT NULL,
   lot_id VARCHAR(18) NOT NULL,
   process VARCHAR(20) NOT NULL,
   process_detail VARCHAR(50) NOT NULL,
   jacket_temp DECIMAL(10,1) NOT NULL,
   content_temp DECIMAL(10,1),
   jacket_pressure DECIMAL(10,3) NOT NULL,
   ambient_temp DECIMAL(10,1) NOT NULL,
   humidity DECIMAL(10,1) NOT NULL,
   PRIMARY KEY (measurement_datetime, lot_id)
);

```

## 注意事項

1. **データ形式**: CSV形式、UTF-8エンコーディング
2. **機密性**: Medium（製造技術ノウハウを含む）
3. **更新頻度**: リアルタイム（製造工程中、1分間隔で自動記録）
4. **アクセス制御**: 製造技術部門、品質管理部門の参照権限が必要

## 更新履歴

| 日付 | バージョン | 変更内容 |
|------|-----------|----------|
| 2025/12/20 | 1.0 | 初版作成 |
