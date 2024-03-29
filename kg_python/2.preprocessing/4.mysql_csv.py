# ------------ 提取zotero的高亮实体和关系，构建mysql.csv文件 --------------

from pyzotero import zotero
from py2neo import Graph, Node
import pandas as pd

library_id = '11562465'
library_type = 'user'
api_key = '0bQwmW6asXU18FIOvFbu2YHN'
locale = 'zh-CN'
# 实例化
zot = zotero.Zotero(library_id, library_type, api_key, locale)

# 拿到所有条目items
items = zot.items()
print(items)

red_name = []
green_desc = []
blue_grammar = []
yellow_belong = []

for item in items:
    # 1. 提取红色实体
    if 'parentItem' in item['data'] \
            and item['data']['parentItem'] == 'UU8THKNR' \
            and 'annotationType' in item['data'] \
            and item['data']['annotationType'] == 'highlight' \
            and item['data']['annotationColor'] == '#ff6666':
        # print(item["data"]["annotationText"])
        red_name.append(item["data"]["annotationText"].replace(" ", ""))

    # 2. 提取绿色实体
    elif 'parentItem' in item['data'] \
            and item['data']['parentItem'] == 'UU8THKNR' \
            and 'annotationType' in item['data'] \
            and item['data']['annotationType'] == 'highlight' \
            and item['data']['annotationColor'] == '#5fb236':
        # print(item["data"]["annotationText"])
        green_desc.append(item["data"]["annotationText"].replace(" ", ""))

    # 3. 提取蓝色实体
    elif 'parentItem' in item['data'] \
            and item['data']['parentItem'] == 'UU8THKNR' \
            and 'annotationType' in item['data'] \
            and item['data']['annotationType'] == 'highlight' \
            and item['data']['annotationColor'] == '#2ea8e5':
        # print(item["data"]["annotationText"])
        blue_grammar.append(item["data"]["annotationText"].replace(" ", ""))

    # 4. 提取归属
    elif 'parentItem' in item['data'] \
            and item['data']['parentItem'] == 'UU8THKNR' \
            and 'annotationComment' in item['data'] \
            and 'annotationType' in item['data'] \
            and item['data']['annotationType'] == 'note':
        # print(item["data"]["annotationComment"])
        yellow_belong.append(item["data"]["annotationComment"].replace(" ", ""))

# 打印四个列表
print(red_name)
print(len(red_name))
print(green_desc)
print(len(green_desc))
print(blue_grammar)
print(len(blue_grammar))
print(yellow_belong)
print(len(yellow_belong))

import csv
from itertools import zip_longest

# 使用zip合并列表
merged_lists = zip_longest(red_name, blue_grammar, yellow_belong)

# 写入CSV文件
csv_file = '../dataset/mysql.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['red_name', 'blue_grammar', 'yellow_belong'])  # 写入表头
    writer.writerows(merged_lists)

print(f'CSV文件 {csv_file} 已创建成功。')
