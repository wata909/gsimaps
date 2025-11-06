#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GeoJSONファイルにスタイル情報を追加するスクリプト
"""

import json

# 入力ファイルと出力ファイルのパス
input_file = 'data/geojson/noto_2500_wgs84.geojson'
output_file = 'data/geojson/noto_2500_wgs84.geojson'

# スタイル設定
style = {
    "_color": "#ff0000",      # 赤（線の色）
    "_weight": 2,             # 線の太さ（ちょっと太め）
    "_fillOpacity": 0,        # 塗りつぶし透明度0
    "_opacity": 0.8           # 線の透明度
}

print(f"読み込み中: {input_file}")

# GeoJSONファイルを読み込み
with open(input_file, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# 各フィーチャーにスタイル情報を追加
feature_count = 0
for feature in geojson_data['features']:
    if 'properties' not in feature:
        feature['properties'] = {}
    
    # スタイル情報を追加
    feature['properties'].update(style)
    feature_count += 1

print(f"処理したフィーチャー数: {feature_count}")

# 修正したGeoJSONを保存
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=2)

print(f"保存完了: {output_file}")
print("\nスタイル設定:")
print(f"  線の色: {style['_color']} (赤)")
print(f"  線の太さ: {style['_weight']}")
print(f"  塗りつぶし透明度: {style['_fillOpacity']}")
print(f"  線の透明度: {style['_opacity']}")
