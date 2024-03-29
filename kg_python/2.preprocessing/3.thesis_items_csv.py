# --------------------- 提取论文侧边条目，根据结构化数据，整理生成csv文件 ----------------------------
# 本模块代码能在jupyter中运行并得到csv目标文件，在pycharm则不行，我也不知道为什么...

import csv
from pyzotero import zotero

library_id = '11562465'
library_type = 'user'
api_key = '0bQwmW6asXU18FIOvFbu2YHN'
locale = 'zh-CN'
# 实例化
zot = zotero.Zotero(library_id, library_type, api_key, locale)
# 拿到所有条目items
items = zot.items()
print(items)

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

# 要保存的数据列表
data = []
for item in items:
    # 只提取期刊文章，也就是论文的pdf
    if 'itemType' in item['data'] and item['data']['itemType'] == 'journalArticle':
        tags = []
        for tag in item['data']['tags']:
            tags.append(tag['tag'])
        str1 = item['data']['abstractNote']
        print(str1)
        data.append({
            'title': item['data']['title'],
            'creators': item['data']['creators'][0]['lastName'] + item['data']['creators'][0]['firstName'],
            'abstractNote': item['data']['abstractNote'].replace(',', '，'),
            'publicationTitle': item['data']['publicationTitle'],
            'date': item['data']['date'],
            'language': item['data']['language'],
            'url': item['data']['url'],
            'libraryCatalog': item['data']['libraryCatalog'],
            'tags': tags
        })

# 指定要保存的文件名
filename = '../dataset/thesis_item.csv'

# 打开文件并写入数据
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    # 写入表头
    writer.writeheader()
    # 写入数据
    writer.writerows(data)

print('CSV 文件已生成:', filename)
