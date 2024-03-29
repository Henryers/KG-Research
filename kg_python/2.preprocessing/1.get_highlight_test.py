# 提取zotero中高亮信息

from pyzotero import zotero

# zotero 的个人知识库相关信息
library_id = '11562465'
library_type = 'user'
api_key = '0bQwmW6asXU18FIOvFbu2YHN'
locale = 'zh-CN'

# 实例化
zot = zotero.Zotero(library_id, library_type, api_key,locale)
items = zot.items()

# 定义4个列表，存储4篇文章的重要句段
orange1 = []
orange2 = []
orange3 = []
orange4 = []

for item in items:
    # print(item['data'])
    # 处理高亮信息
    if 'annotationType' in item['data'] \
            and item['data']['annotationType'] == 'highlight' \
            and item['data']['parentItem'] == 'UW227V2I' \
            and item['data']['annotationColor'] == '#f19837':
        # print(item['data'])
        orange1.append(item['data']['annotationText'])
    elif 'annotationType' in item['data'] \
            and item['data']['annotationType'] == 'highlight' \
            and item['data']['parentItem'] == '7AMGANSZ' \
            and item['data']['annotationColor'] == '#f19837':
        # print(item['data'])
        orange2.append(item['data']['annotationText'])
    elif 'annotationType' in item['data'] \
            and item['data']['annotationType'] == 'highlight' \
            and item['data']['parentItem'] == 'CNET2VHR' \
            and item['data']['annotationColor'] == '#f19837':
        # print(item['data'])
        orange3.append(item['data']['annotationText'])
    elif 'annotationType' in item['data'] \
            and item['data']['annotationType'] == 'highlight' \
            and item['data']['parentItem'] == 'X3LX2YEF' \
            and item['data']['annotationColor'] == '#f19837':
        # print(item['data'])
        orange4.append(item['data']['annotationText'])
    else:
        pass

print("橙色重要句段：")
for i in orange1:
    new_i = str(i)
    print(new_i.replace(' ', ''))
print("------------------------------------------------------")
for i in orange2:
    new_i = str(i)
    print(new_i.replace(' ', ''))
print("------------------------------------------------------")
for i in orange3:
    new_i = str(i)
    print(new_i.replace(' ', ''))
print("------------------------------------------------------")
for i in orange4:
    new_i = str(i)
    print(new_i.replace(' ', ''))
