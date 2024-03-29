# -------------- 数学知识图谱 -----------------
# 利用正则表达式来提取 obsidian 中笔记的实体和关系，构建三元组存入neo4j

import re
from py2neo import Graph, Node

# 连接图数据库
graph = Graph("bolt://localhost:7687/", auth=(
    'neo4j', '20040111'), name='maths')


# --------------------分类提取实体函数------------------------
def extract_label_entities_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # 读取markdown格式的文本
        content = file.read()
        # print(content)
    entities = []
    lines = content.strip().split('\n')  # 将文本按行拆分为列表
    # print(lines)
    # 按行遍历
    for line in lines:
        line = line.strip()  # 去除行尾的换行符和空白字符
        # print(line)
        # 只选择该行第一个** **包裹的实体，才确定是本文件的
        match = re.search(r'\*\*([^*]+)\*\*', line)
        if match:
            # print(match.group(1))
            entities.append(match.group(1))

    return entities


# 三个文件
high_maths = "../dataset/high_maths.md"
linear_maths = "../dataset/linear_maths.md"
dis_maths = "../dataset/dis_maths.md"

# 带高等数学标签的实体
high_maths_entities = []
high_maths_entities += extract_label_entities_from_markdown(high_maths)
# print(high_maths_entities)

# 带线性代数标签的实体
linear_maths_entities = []
linear_maths_entities += extract_label_entities_from_markdown(linear_maths)
# print(linear_maths_entities)

# 带高等数学标签的实体
dis_maths_entities = []
dis_maths_entities += extract_label_entities_from_markdown(dis_maths)
# print(dis_maths_entities)

# 打开多个文件进行相同操作
file_paths = [high_maths, linear_maths, dis_maths]

# --------------存放关系两端实体的二元列表型数组，每个元素be like:  ['x','y']  ----------------------
# 初始化二元关系数组
rels_double_entities = []
# 遍历三个文件,按行遍历,拿到每一行的二元关系
for file_path in file_paths:
    with open(file_path, "r", encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 去除行尾的换行符和空白字符
            # 在这里进行对每一行的处理,如果该行有这两个特殊字符,说明有链接关系,才进行下一步二元关系抽取操作
            if '^' in line and '[' in line:
                double_entities = r'\*\*([^\*]+)\*\*'
                # 临时的小列表，存放二元关系进入数组用的，每循环一次都要初始化一次
                matches = []
                matches += re.findall(double_entities, line)
                # print(line)  # 打印每一行的内容
                # print(matches)
                # 一个实体链接一个/多个目标实体
                for i in range(1, len(matches)):
                    rels_double_entities.append([matches[0], matches[i]])
print(rels_double_entities)

graph.run('MATCH p=()-->() delete p')
graph.run('MATCH (n) delete n')
# neo4j中创建实体
for each in high_maths_entities:
    node = Node('高等数学', name=each)
    graph.create(node)
    # print('创建实体 {}'.format(each))
for each in linear_maths_entities:
    node = Node('线性代数', name=each)
    graph.create(node)
    # print('创建实体 {}'.format(each))
for each in dis_maths_entities:
    node = Node('离散数学', name=each)
    graph.create(node)
    # print('创建实体 {}'.format(each))


# 定义创建关系函数
def create_relationship(start_node, end_node, edges, rel_type, rel_name):
    # 5个参数分别为：起始节点，终止节点，关系，关系类型，关系属性名称name
    for edge in edges:  # 二元关系列表  be like:   ['药物厂商','具体药物']
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
            # print('创建关系 {}-{}->{}'.format(p, rel_type, q))
        except Exception as e:  # Exception表示捕获所有异常，并将其打包为e
            print(e)  # 将错误信息打印出来


# 调用函数,创建关系
create_relationship('高等数学', '高等数学', rels_double_entities, 'rels_knowledge', 'rels_knowledge')
create_relationship('高等数学', '线性代数', rels_double_entities, 'rels_knowledge', 'rels_knowledge')
create_relationship('高等数学', '离散数学', rels_double_entities, 'rels_knowledge', 'rels_knowledge')
create_relationship('线性代数', '高等数学', rels_double_entities, 'rels_knowledge', 'rels_knowledge')
create_relationship('线性代数', '线性代数', rels_double_entities, 'rels_knowledge', 'rels_knowledge')
create_relationship('线性代数', '离散数学', rels_double_entities, 'rels_knowledge', 'rels_knowledge')
create_relationship('离散数学', '高等数学', rels_double_entities, 'rels_knowledge', 'rels_knowledge')
create_relationship('离散数学', '线性代数', rels_double_entities, 'rels_knowledge', 'rels_knowledge')
create_relationship('离散数学', '离散数学', rels_double_entities, 'rels_knowledge', 'rels_knowledge')

# 对二维列表rels_double_entities进行遍历
for item in rels_double_entities:
    print(item[0], item[1])
