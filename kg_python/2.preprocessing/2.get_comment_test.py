# 提取zotero中注释信息

from pyzotero import zotero

library_id = '11562465'
library_type = 'user'
api_key = '0bQwmW6asXU18FIOvFbu2YHN'
locale = 'zh-CN'
# 实例化
zot = zotero.Zotero(library_id, library_type, api_key, locale)
items = zot.items()

for item in items:
    # 处理注释信息
    if 'annotationType' in item['data'] and item['data']['annotationType'] == 'note':
        note = item['data']['annotationComment']
        print("注释为：" + note)
    else:
        pass
