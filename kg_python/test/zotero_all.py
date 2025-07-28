"""
所有zotero中的条目信息
"""

import csv
from pyzotero import zotero

library_id = '11562465'
library_type = 'user'
api_key = '0bQwmW6asXU18FIOvFbu2YHN'
locale = 'zh-CN'
# 实例化
zot = zotero.Zotero(library_id, library_type, api_key, locale)

# 初始化一个列表来存储所有条目
all_items = []

# 初始化分页参数
start = 0
items_per_page = 100

# 循环获取所有条目items数据
while True:
    # 获取当前页的数据
    items = zot.items(limit=items_per_page, start=start)
    if not items:
        break  # 如果没有更多数据，退出循环
    all_items.extend(items)  # 将当前页的数据添加到列表中
    start += items_per_page  # 更新分页参数

print(len(all_items))

# 构建csv文件
# 要保存的字段列表
fields = [
    'title',
    'creators',
    'abstractNote',
    'publicationTitle',
    'date',
    'language',
    'url',
    'libraryCatalog',
    'tags'
]


# 'annotation', 'document', 'thesis', 'preprint', 'webpage', 'attachment', 'conferencePaper', 'book', 'journalArticle'

# 要保存的数据列表
data = []
for item in all_items:
    # print(item['data']['itemType'])
    # 只提取期刊文章，也就是论文的pdf
    if 'itemType' in item['data'] and (item['data']['itemType'] == 'preprint'):
        tags = []
        print(item['data'])
    #     for tag in item['data']['tags']:
    #         tags.append(tag['tag'])
    #     str1 = item['data']['abstractNote']
    #     print(str1)
    #     data.append({
    #         'title': item['data']['title'],
    #         'creators': item['data']['creators'][0]['lastName'] + item['data']['creators'][0]['firstName'],
    #         'abstractNote': item['data']['abstractNote'].replace(',', '，'),
    #         'publicationTitle': item['data']['publicationTitle'],
    #         'date': item['data']['date'],
    #         'language': item['data']['language'],
    #         'url': item['data']['url'],
    #         'libraryCatalog': item['data']['libraryCatalog'],
    #         'tags': tags
    #     })

print(data)

# # 指定要保存的文件名
# filename = '../dataset/thesis_item_0725.csv'
#
# # 打开文件并写入数据
# with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=fields)
#     # 写入表头
#     writer.writeheader()
#     # 写入数据
#     writer.writerows(data)
#
# print('CSV 文件已生成:', filename)