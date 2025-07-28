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
# 拿到所有条目items
items = zot.items()
print(items)