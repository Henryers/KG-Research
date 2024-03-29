# ------------- zotero知识图谱(有前端展示) -------------
# 以树结构来展示zotero中的实体与关系图，构建三元组并存入neo4j

from pyzotero import zotero
from py2neo import Graph, Node

# 连接图数据库
graph = Graph("bolt://localhost:7687/", auth=(
    'neo4j', '20040111'), name='zotero1')

# 连接zotero个人知识库的相关信息
library_id = '11562465'
library_type = 'user'
api_key = '0bQwmW6asXU18FIOvFbu2YHN'
locale = 'zh-CN'
# 实例化
zot = zotero.Zotero(library_id, library_type, api_key, locale)
# 获取所有数据
items = zot.everything(zot.items())
# print(len(items))

# 1. 创建实体(略，已经有实体了，下面直接neo4j创建实体，还带标签)

# 2. 创建关系
pdf_name = []
red_name = []
green_desc = []
blue_grammar = []
yellow_comment = []
others = []

dist_pdfs = {}
dist_notes = {}
key_replacements = {}
count_son = 0
for i in items:
    # 使用 get 方法安全地访问 'parentItem' 键(否则如果不存在直接报错，下面的运行不了)
    parent_item = i['data'].get('parentItem')
    if parent_item:
        count_son += 1
        if 'annotationText' not in i['data']:
            # 1. 注释部分：直接加入comment这部分的列表
            if 'annotationComment' in i['data']:
                dist_notes[i['data']['annotationComment']] = parent_item
                yellow_comment.append(i['data']['annotationComment'])
            else:
                # pdf论文不是根标签，因为上面还被一个论文（含条目）的文件夹包住了，变成类似中间件的位置
                # 那就把dist_pdfs的key改了！，这个中间件的key才能跟子节点的高亮注释产生直接联系！
                # 被替换的key对应的东西，存储着条目信息，放在条目知识图片那边（两个图谱关联之后再说）
                key_replacements[i['data']['parentItem']] = i['key']
        else:
            dist_notes[i['data']['annotationText']] = parent_item
            # 2.高亮部分：分类讨论加入不同标签的实体列表
            if i['data']['annotationColor'] == '#ff6666':
                red_name.append(i['data']['annotationText'])
            elif i['data']['annotationColor'] == '#5fb236':
                green_desc.append(i['data']['annotationText'])
            elif i['data']['annotationColor'] == '#2ea8e5':
                blue_grammar.append(i['data']['annotationText'])
            elif i['data']['annotationColor'] == '#ffd400':
                yellow_comment.append(i['data']['annotationText'])
            else:
                others.append(i['data']['annotationText'])
    else:
        dist_pdfs[i['key']] = i['data']['title']
        pdf_name.append(i['data']['title'])

# 更新dist_pdf
dist_pdfs = {key_replacements.get(key, key): value for key, value in dist_pdfs.items()}
list_all = []
for key1, value1 in dist_pdfs.items():
    for key2, value2 in dist_notes.items():
        if value2 == key1:
            list_all.append([value1, key2])
for i in pdf_name:
    list_all.append(['zotero', i])
print(list_all)

# 3. neo4j 创建实体
graph.run('MATCH p=()-->() delete p')
graph.run('MATCH (n) delete n')

# 总结点
node = Node('zotero', name='zotero')
graph.create(node)
for each in pdf_name:
    node = Node('pdf', name=each)
    graph.create(node)
for each in red_name:
    node = Node('entity', name=each)
    graph.create(node)
for each in green_desc:
    node = Node('description', name=each)
    graph.create(node)
for each in blue_grammar:
    node = Node('grammar', name=each)
    graph.create(node)
for each in yellow_comment:
    node = Node('comment', name=each)
    graph.create(node)
for each in others:
    node = Node('others', name=each)
    graph.create(node)

# 4. neo4j创建关系
def create_relationship(start_node, end_node, edges, rel_type, rel_name):
    # 5个参数分别为：起始节点，终止节点，关系，关系类型，关系属性名称name
    for edge in edges:   # 关系列表edges中的元素 be like: ['药物厂商','具体药物']
        p = edge[0]      # 获取关系起始点的名称  be like: p='药物厂商'
        q = edge[1]      # 获取关系终止点的名称  be like: p='具体药物'
        # 创建关系的 Cypher 语句
        query = r"match(p:%s),(q:%s) where p.name='%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" \
                % (start_node, end_node, p, q, rel_type, rel_name)
        # cypher语句be like:
        # match(p:start_node),(q:end_node) where p.name=p and q.name=q
        # //确保在相应标签中找到的两个具体节点名称跟p.q的一样，才符合要求
        # create (p)-[rel:rel_type{name:'rel_name'}]->(q)
        # //关系为rel_type,其name属性为rel_name
        try:
            graph.run(query)     # 每构建一条关系语句后，就直接尝试运行 Cypher 语句
            # print('创建关系 {}-{}->{}'.format(p, rel_type, q))
        except Exception as e:   # Exception表示捕获所有异常，并将其打包为e
            print(e)             # 将错误信息打印出来

# 通过调用函数创建所有关系(执行语句在函数中以及出现)
create_relationship('zotero', 'pdf', list_all, 'pdf', 'pdf')
create_relationship('pdf', 'entity', list_all, 'entity', '专有名词')
create_relationship('pdf', 'description', list_all, 'description', '描述')
create_relationship('pdf', 'grammar', list_all, 'grammar', '语法')
create_relationship('pdf', 'comment', list_all, 'comment', '注释')
create_relationship('pdf', 'others', list_all, 'others', '其他')