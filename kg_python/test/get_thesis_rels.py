"""
论文条目知识图谱
利用pandas处理(2.3 thesis_items_csv.py预处理得到的) thesis_item.csv文件，提取其中的实体关系构建三元组，利用py2neo编写cypher语句存入neo4j
"""

from py2neo import Graph, Node
from collections import defaultdict
import pandas as pd

# 连接图数据库
graph = Graph("bolt://localhost:7687/", auth=(
    'neo4j', '20040111'), name='zoteroThesis')

df = pd.read_csv('../dataset/thesis_item_0725.csv')
# print(df.shape)  # 返回一个元组, (行数,列数)
# print(df.head())  # 默认返回csv数据框的前五行，便于用户快速浏览数据(也可以在()中输入数字，指定返回的行数)

# 1.--------------------------------提取实体---------------------------------------

# 先定义一个列表
title = []
# 遍历'title'这一列的每一个元素
for each in df['title']:
    # 按照,分割每一个元素，并将分割后的子字符串用extend的形式，全都传给symptoms列表中
    title.extend(each.split(','))
# 列表元素全部添加完成后，将列表强转为集合形式，从而去除其中的重复元素
title = set(title)

# 再提取别的列，思路同上
creators = []
for each in df['creators']:
    creators.extend(each.split(','))
creators = set(creators)

abstractNote = []
for each in df['abstractNote']:
    if isinstance(each, float):
        ...
    else:
        abstractNote.extend(each.split(','))
abstractNote = set(abstractNote)

publicationTitle = []
for each in df['publicationTitle']:
    if not isinstance(each, float):
        publicationTitle.extend(each.split(','))
publicationTitle = set(publicationTitle)

date = []
for each in df['date']:
    # 整数? 先转成字符串再说！
    each_str = str(each)
    date.append(each)
date = set(date)

language = []
for each in df['language']:
    if not isinstance(each, float):
        language.extend(each.split(','))
language = set(language)

url = []
for each in df['url']:
    if isinstance(each, float):
        ...
    else:
        url.extend(each.split(','))
url = set(url)

libraryCatalog = []
for each in df['libraryCatalog']:
    if not isinstance(each, float):
        libraryCatalog.extend(each.strip("[ ]").split(','))
libraryCatalog = set(libraryCatalog)

tags = []
for each in df['tags']:
    for item in eval(each):
        tags.append(item)
tags = set(tags)


# 2.--------------------------------提取关系（边）------------------------------------
def deduplicate(rels_old):
    '''关系去重函数'''
    rels_new = []  # 定义空的新列表
    for each in rels_old:  # 遍历旧列表   (含重复元素)
        if each not in rels_new:  # 如果元素不在新列表中
            rels_new.append(each)  # 那就追加写进去(如果在，就不执行任何操作)
    return rels_new  # 返回新列表   (不含重复元素)


# 关系：标题-作者
rels_creators = []
for idx, row in df.iterrows():  # 按行遍历，拿到每一行的行号idx,和每一行的数据row
    # 切片后可能有多个子字符串each(所以需要遍历，让该行的title跟多个creators组成多个二元关系)
    for each in row['creators'].split(','):
        rels_creators.append([row['title'], each])
        # 将该行疾病名称和对应的检查项目组成一个二/多元关系，追加写入rels_creators中
rels_creators = deduplicate(rels_creators)  # 对所有关系进行去重操作
# 返回的 rels_creators 就是一个不含重复关系的列表，其中每个元素是形如 [title, creator] 的二元关系
# 或者是[title, creator1],[title, creator2...] 的二元关系
# print(rels_creators)

# 构建别的关系，思路跟上面一样
# 标题-摘要
rels_abstractNote = []
for idx, row in df.iterrows():
    if not isinstance(row['abstractNote'], float):
        for each in row['abstractNote'].split(','):
            rels_abstractNote.append([row['title'], each])
rels_abstractNote = deduplicate(rels_abstractNote)
print()
print()
# print(rels_abstractNote)

# 标题-期刊
rels_publicationTitle = []
for idx, row in df.iterrows():
    if not isinstance(row['publicationTitle'], float):
        for each in row['publicationTitle'].split(','):
            rels_publicationTitle.append([row['title'], each])
rels_publicationTitle = deduplicate(rels_publicationTitle)
print()
print()
# print(rels_publicationTitle)

# 期刊-文库编目
rels_libraryCatalog = []
for idx, row in df.iterrows():
    if not isinstance(row['libraryCatalog'], float):
        for each in row['libraryCatalog'].split(','):
            if not isinstance(row['publicationTitle'], float):
                rels_libraryCatalog.append([row['publicationTitle'], each])
rels_libraryCatalog = deduplicate(rels_libraryCatalog)
print()
print()
print(rels_libraryCatalog)

# 标题-日期
rels_date = []
for idx, row in df.iterrows():
    # 注意日期是int整数，没有split方法，也不可迭代，需要转换为字符串！
    date_str = str(row['date'])  # 将整数转换为字符串
    for each in date_str.split(','):
        rels_date.append([row['title'], each])
rels_date = deduplicate(rels_date)
print()
print()
# print(rels_date)

# 标题-网址
rels_url = []
for idx, row in df.iterrows():
    if not isinstance(row['url'], float):
        for each in row['url'].split(','):
            rels_url.append([row['title'], each])
rels_url = deduplicate(rels_url)
print()
print()
# print(rels_url)

# 标题-语言
rels_language = []
for idx, row in df.iterrows():
    if not isinstance(row['language'], float):
        for each in row['language'].split(','):
            rels_language.append([row['title'], each])
rels_language = deduplicate(rels_language)
print()
print()
# print(rels_language)

# 标题-标签
rels_tags = []
for idx, row in df.iterrows():
    # 这一整行的tags列，为一个列表形式的字符串，转化为列表，再一个个拿出来
    true_list = eval(row['tags'])
    for each in true_list:
        rels_tags.append([row['title'], each])
rels_tags = deduplicate(rels_tags)
print()
print()
# print(rels_tags)

