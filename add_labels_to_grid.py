#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
グリッドGeoJSONに中心点のラベルを追加するスクリプト
"""

import json

def calculate_polygon_centroid(coordinates):
    """ポリゴンの重心を計算（外周のみ）"""
    # coordinates[0]が外周
    ring = coordinates[0]
    
    # 重心計算（単純平均）
    sum_x = 0
    sum_y = 0
    count = len(ring) - 1  # 最後の点は最初と同じなので除外
    
    for i in range(count):
        sum_x += ring[i][0]
        sum_y += ring[i][1]
    
    centroid_x = sum_x / count
    centroid_y = sum_y / count
    
    return [centroid_x, centroid_y]

# 入力ファイルと出力ファイルのパス
input_file = 'data/geojson/noto_2500_wgs84.geojson'
output_grid_file = 'data/geojson/noto_2500_wgs84_grid.geojson'  # グリッド用
output_label_file = 'data/geojson/noto_2500_wgs84_labels.geojson'  # ラベル用

print(f"読み込み中: {input_file}")

# GeoJSONファイルを読み込み
with open(input_file, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# 元のポリゴンフィーチャー数
original_count = len(geojson_data['features'])
print(f"元のフィーチャー数: {original_count}")

# グリッド用とラベル用のフィーチャーリスト
grid_features = []
label_features = []

# 各ポリゴンに対して中心点のラベルを追加
for feature in geojson_data['features']:
    # グリッド用（ポリゴン）
    grid_features.append(feature)
    
    # ポリゴンの中心点を計算
    centroid = calculate_polygon_centroid(feature['geometry']['coordinates'])
    
    # ラベル用のPointフィーチャーを作成
    label_feature = {
        "type": "Feature",
        "properties": {
            "code": feature['properties']['code'],
            "_markerType": "DivIcon",
            "_html": f"<div style='font-size: 10px; color: #ff0000; font-weight: bold; text-shadow: 1px 1px 2px white, -1px -1px 2px white, 1px -1px 2px white, -1px 1px 2px white; white-space: nowrap;'>{feature['properties']['code']}</div>",
            "_iconSize": [60, 20],
            "_iconAnchor": [30, 10]
        },
        "geometry": {
            "type": "Point",
            "coordinates": centroid
        }
    }
    
    label_features.append(label_feature)

# グリッド用GeoJSON
grid_geojson = {
    "type": "FeatureCollection",
    "name": "noto_2500_wgs84_grid",
    "crs": geojson_data['crs'],
    "features": grid_features
}

# ラベル用GeoJSON
label_geojson = {
    "type": "FeatureCollection",
    "name": "noto_2500_wgs84_labels",
    "crs": geojson_data['crs'],
    "features": label_features
}

print(f"グリッド数: {len(grid_features)}, ラベル数: {len(label_features)}")

# グリッド用ファイルを保存
with open(output_grid_file, 'w', encoding='utf-8') as f:
    json.dump(grid_geojson, f, ensure_ascii=False, indent=2)

# ラベル用ファイルを保存
with open(output_label_file, 'w', encoding='utf-8') as f:
    json.dump(label_geojson, f, ensure_ascii=False, indent=2)

print(f"グリッド保存完了: {output_grid_file}")
print(f"ラベル保存完了: {output_label_file}")
print("\nラベル設定:")
print("  表示開始ズームレベル: 12")
print("  ラベル内容: codeプロパティの値")
print("  位置: 各グリッドの中心")
