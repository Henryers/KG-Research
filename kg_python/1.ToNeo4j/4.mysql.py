# -------------- 数据库知识图谱 --------------
# 利用pandas处理(4.mysql_csv.py预处理得到的)csv文件，提取其中的实体关系构建三元组，利用py2neo编写cypher语句存入neo4j

from py2neo import Graph, Node
import pandas as pd

# 连接图数据库
graph = Graph("bolt://localhost:7687/", auth=(
    'neo4j', '20040111'), name='mysql')

df = pd.read_csv('../dataset/mysql.csv')
print(df.shape)    # 返回一个元组, (行数,列数)
print(df.head())   # 默认返回csv数据框的前五行，便于用户快速浏览数据(也可以在()中输入数字，指定返回的行数)

# 1.--------------------------------提取实体---------------------------------------
# 1.先试一下提取症状
# 先定义一个列表
titles = []
# 遍历'症状'这一列的每一个元素
for each in df['名称']:
    # 按照,分割每一个元素，并将分割后的子字符串用extend的形式，全都传给symptoms列表中
    titles.extend(each.split(','))
# 列表元素全部添加完成后，将列表强转为集合形式，从而去除其中的重复元素
titles = set(titles)
# print(symptoms)   # 打印所有'症状'实体

# 2.再试一下提取科室(思路同上)
desc = []
for each in df['说明']:
    desc.extend(each.split(','))
desc = set(desc)
# print(department)

# 3.检查(以下均为照抄)
belong = []
for each in df['归属']:
    belong.extend(each.split(','))
belong = set(belong)
# print(checks)

# 4.字典信息
mysql_infos = [] # 疾病信息
for idx, row in df.iterrows():  # 按行遍历，拿到每一行的行号idx,和每一行的数据row
    mysql_infos.append(dict(row))
    # 将一行数据转化为字典形式，该行每个数据作为键值对的值，对应的列号作为键key，再追加写入disease_infos列表中
    # 即列表中的元素是字典类型，每个元素都是一个字典(且一个字典又由多个键值对组成)
    # dict()字典强转这个操作，本身就把该行row的每个元素对应的列号作为键key
dict(row).keys()   # 将键key进行返回


# 2.--------------------------------提取关系（边）------------------------------------
'''关系去重函数'''
def deduplicate(rels_old):

    rels_new = []                   # 定义空的新列表
    for each in rels_old:           # 遍历旧列表   (含重复元素)
        if each not in rels_new:    # 如果元素不在新列表中
            rels_new.append(each)   # 那就追加写进去(如果在，就不执行任何操作)
    return rels_new                 # 返回新列表   (不含重复元素)

# 1.关系：名称-说明
rels_desc = []
for idx, row in df.iterrows():            # 按行遍历，拿到每一行的行号idx,和每一行的数据row
    for each in row['说明'].split(','):
        rels_desc.append([row['名称'], each])
        # 将该行疾病名称和对应的检查项目组成一个二/多元关系，追加写入rels_check中
rels_check = deduplicate(rels_desc)      # 对所有关系进行去重操作
# 返回的 rels_check 就是一个不含重复关系的列表，其中每个元素是形如 [疾病名称, 某个检查项目] 的二元关系
# 或者是[疾病名称, 某个检查项目1],[疾病名称, 某个检查项目2...] 的二元关系
print(rels_desc)

# 2.关系：名称-归属
rels_belong = []
for idx, row in df.iterrows():
    for each in row['归属'].split(','):
        rels_belong.append([row['名称'], each])
rels_symptom = deduplicate(rels_belong)
print(rels_belong)

# 3.关系：说明-归属
rels_desc_belong = []
for idx, row in df.iterrows():
    for each in row['归属'].split(','):
        rels_desc_belong.append([row['说明'], each])
rels_acompany = deduplicate(rels_desc_belong)


# ----------------------------neo4j数据库清空，进行初始化--------------------------------
graph.run('MATCH p=()-->() delete p')
graph.run('MATCH (n) delete n')
# 3.--------------------------------创建实体到neo4j------------------------------------
# 创造疾病实体
count = 0
# 按行遍历，每次取出列表的一行(即一个字典)
for disease_dict in mysql_infos:
    try:
        # 使用Node()语法创建节点，其中第一个参数为标签名，第二个参数为标签属性
        node = Node("Disease",                    # disease节点
                    name=disease_dict['疾病名称'],  # 将该字典中键key为'疾病名称'的对应值取出，赋值给name
                    desc=disease_dict['疾病描述'],  # 下面都同理(都是disease节点的属性)
                    prevent=disease_dict['预防措施'],
                    cause=disease_dict['病因'],
                    easy_get=disease_dict['易感人群'],
                    cure_lasttime=disease_dict['疗程'],
                    cure_department=disease_dict['科室'],
                    cure_way=disease_dict['疗法'],
                    cured_prob=disease_dict['治愈率'])
        graph.create(node)    # 直接利用py2neo的.create()创建节点，不用自己拼接字符串了，好耶！！！
        count += 1
        print('创建疾病实体：', disease_dict['疾病名称'])
    except:     # 保证代码健壮性罢了(上面的提取可能遇到数据缺失而报错，这里直接忽略/跳过报错，执行下行提取)
        pass
print('共创建 {} 个疾病实体'.format(count))
# 创建药物实体 (与上面类似，只不过节点属性只有一个name而已)
for each in titles:
    node = Node('Title', name=each)
    graph.create(node)
    # print('创建实体 {}'.format(each))
# 创建食物实体 (同理)
for each in desc:
    node = Node('Desc', name=each)
    graph.create(node)
    # print('创建实体 {}'.format(each))
# 创建检查实体
for each in belong:
    node = Node('Belong', name=each)
    graph.create(node)
    # print('创建实体 {}'.format(each))


# 4.--------------------------------创建关系到neo4j--------------------------------------
# 定义创建关系函数
def create_relationship(start_node, end_node, edges, rel_type, rel_name):
    # 5个参数分别为：起始节点，终止节点，关系，关系类型，关系属性名称name
    '''创建关系函数'''
    for edge in edges:   # 关系列表edges中的元素be like:   ['药物厂商','具体药物']
        p = edge[0]      # 获取关系起始点的名称  be like: p='药物厂商'
        q = edge[1]      # 获取关系终止点的名称  be like: p='具体药物'
        # 创建关系的 Cypher 语句
        query = "match(p:%s),(q:%s) where p.name='%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" \
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
create_relationship('Title', 'Desc', rels_desc, 'rels_desc', '推荐食谱')
# 在Disease和Food两个标签中，根据rels_recommandeat寻找能匹配上的两端节点，并进行关系创建连接
# 其中关系名为'recommand_eat',关系属性为'推荐食谱'(下面关系同理)
create_relationship('Title', 'Belong', rels_belong, 'rels_belong', '忌吃')
# create_relationship('Desc', 'Belong', rels_desc_belong, 'rels_desc_belong', '忌吃')