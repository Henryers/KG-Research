# -------------- 论文条目知识图谱 ----------------
# 利用pandas处理(3.thesis_items_csv.py预处理得到的)csv文件，提取其中的实体关系构建三元组，利用py2neo编写cypher语句存入neo4j

from py2neo import Graph, Node
from collections import defaultdict
import pandas as pd

# 连接图数据库
graph = Graph("bolt://localhost:7687/", auth=(
    'neo4j', '20040111'), name='thesisitems')

df = pd.read_csv('../dataset/thesis_item.csv')
print(df.shape)  # 返回一个元组, (行数,列数)
print(df.head())  # 默认返回csv数据框的前五行，便于用户快速浏览数据(也可以在()中输入数字，指定返回的行数)

# 1.--------------------------------提取实体---------------------------------------

# 先定义一个列表
title = []
# 遍历'title'这一列的每一个元素
for each in df['title']:
    # 按照,分割每一个元素，并将分割后的子字符串用extend的形式，全都传给symptoms列表中
    title.extend(each.split(','))
# 列表元素全部添加完成后，将列表强转为集合形式，从而去除其中的重复元素
title = set(title)
print(title)  # 打印所有'标题'实体

# 再提取别的列，思路同上
creators = []
for each in df['creators']:
    creators.extend(each.split(','))
creators = set(creators)
print(creators)

abstractNote = []
for each in df['abstractNote']:
    abstractNote.extend(each.split(','))
abstractNote = set(abstractNote)
print(abstractNote)

publicationTitle = []
for each in df['publicationTitle']:
    publicationTitle.extend(each.split(','))
publicationTitle = set(publicationTitle)
print(publicationTitle)

date = []
for each in df['date']:
    # 整数? 先转成字符串再说！
    each_str = str(each)
    date.append(each)
date = set(date)
print(date)

language = []
for each in df['language']:
    language.extend(each.split(','))
language = set(language)
print(language)

url = []
for each in df['url']:
    url.extend(each.split(','))
url = set(url)
print(url)

libraryCatalog = []
for each in df['libraryCatalog']:
    libraryCatalog.extend(each.strip("[ ]").split(','))
libraryCatalog = set(libraryCatalog)
print(libraryCatalog)

tags = []
for each in df['tags']:
    print(each)
    for item in eval(each):
        print(item)
        tags.append(item)
tags = set(tags)
print(tags)


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
print(rels_creators)

# 构建别的关系，思路跟上面一样
# 标题-摘要
rels_abstractNote = []
for idx, row in df.iterrows():
    for each in row['abstractNote'].split(','):
        rels_abstractNote.append([row['title'], each])
rels_abstractNote = deduplicate(rels_abstractNote)
print(rels_abstractNote)
# 标题-期刊
rels_publicationTitle = []
for idx, row in df.iterrows():
    for each in row['publicationTitle'].split(','):
        rels_publicationTitle.append([row['title'], each])
rels_publicationTitle = deduplicate(rels_publicationTitle)
print(rels_publicationTitle)
# 期刊-文库编目
rels_libraryCatalog = []
for idx, row in df.iterrows():
    for each in row['libraryCatalog'].split(','):
        rels_libraryCatalog.append([row['publicationTitle'], each])
rels_libraryCatalog = deduplicate(rels_libraryCatalog)
print(rels_libraryCatalog)
# 标题-日期
rels_date = []
for idx, row in df.iterrows():
    # 注意日期是int整数，没有split方法，也不可迭代，需要转换为字符串！
    date_str = str(row['date'])  # 将整数转换为字符串
    for each in date_str.split(','):
        rels_date.append([row['title'], each])
rels_date = deduplicate(rels_date)
print(rels_date)
# 标题-网址
rels_url = []
for idx, row in df.iterrows():
    for each in row['url'].split(','):
        rels_url.append([row['title'], each])
rels_url = deduplicate(rels_url)
print(rels_url)
# 标题-语言
rels_language = []
for idx, row in df.iterrows():
    for each in row['language'].split(','):
        rels_language.append([row['title'], each])
rels_language = deduplicate(rels_language)
print(rels_language)
# 标题-标签
rels_tags = []
for idx, row in df.iterrows():
    # 这一整行的tags列，为一个列表形式的字符串，转化为列表，再一个个拿出来
    true_list = eval(row['tags'])
    for each in true_list:
        rels_tags.append([row['title'], each])
rels_tags = deduplicate(rels_tags)
print(rels_tags)

# 3.--------------------------------创建实体到neo4j------------------------------------
# neo4j数据库清空，进行初始化
graph.run('MATCH p=()-->() delete p')
graph.run('MATCH (n) delete n ')

# 创建title节点
# 按行遍历，每次取出列表的一行(即一个字典)
for each in title:
    # 使用Node()语法创建节点，其中第一个参数为标签名，第二个参数为标签属性
    node = Node('title', name=each)
    graph.create(node)
# 同理创建其他节点
for each in creators:
    node = Node('creators', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
for each in abstractNote:
    node = Node('abstractNote', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
for each in publicationTitle:
    node = Node('publicationTitle', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
for each in date:
    each_str = str(each)
    node = Node('date', name=each_str)
    graph.create(node)
    print('创建实体 {}'.format(each_str))
for each in language:
    node = Node('language', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
for each in url:
    node = Node('url', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
for each in libraryCatalog:
    node = Node('libraryCatalog', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
for each in tags:
    node = Node('tags', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))


# 4.--------------------------------创建关系到neo4j------------------------------------
# 定义创建关系函数
def create_relationship(start_node, end_node, edges, rel_type, rel_name):
    # 5个参数分别为：起始节点，终止节点，关系，关系类型，关系属性名称name
    '''创建关系函数'''
    for edge in edges:  # 关系列表edges中的元素be like:   ['药物厂商','具体药物']
        p = edge[0]  # 获取关系起始点的名称  be like: p='药物厂商'
        q = edge[1]  # 获取关系终止点的名称  be like: p='具体药物'
        # 创建关系的 Cypher 语句
        query = "match(p:%s),(q:%s) where p.name='%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" \
                % (start_node, end_node, p, q, rel_type, rel_name)
        # cypher语句be like:
        # match(p:start_node),(q:end_node) where p.name=p and q.name=q
        # //确保在相应标签中找到的两个具体节点名称跟p.q的一样，才符合要求
        # create (p)-[rel:rel_type{name:'rel_name'}]->(q)
        # //关系为rel_type,其name属性为rel_name
        try:
            graph.run(query)  # 每构建一条关系语句后，就直接尝试运行 Cypher 语句
            print('创建关系 {}-{}->{}'.format(p, rel_type, q))
        except Exception as e:  # Exception表示捕获所有异常，并将其打包为e
            print(e)  # 将错误信息打印出来


# 通过函数创建所有关系(执行语句在函数中以及出现)
create_relationship('title', 'creators', rels_creators, 'creators', '文章作者')
# 在title和creators两个标签中，根据rels_creators寻找能匹配上的两端节点，并进行关系创建连接
# 其中关系名为'creators',关系属性为'文章作者'(下面关系同理)
create_relationship('title', 'abstractNote', rels_abstractNote, 'abstractNote', '摘要')
create_relationship('title', 'publicationTitle', rels_publicationTitle, 'publicationTitle', '期刊')
create_relationship('publicationTitle', 'libraryCatalog', rels_libraryCatalog, 'libraryCatalog', '摘要')
create_relationship('title', 'date', rels_date, 'date', '出版日期')
create_relationship('title', 'url', rels_url, 'url', '对应网址')
create_relationship('title', 'language', rels_language, 'language', '文章语言')
create_relationship('title', 'tags', rels_tags, 'tags', '相关标签')
