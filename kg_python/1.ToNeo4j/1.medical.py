# -------------- 医疗知识图谱(有前端展示) -----------------
# 利用pandas处理网上获取的medical.csv文件，提取其中的实体关系构建三元组，利用py2neo编写cypher语句存入neo4j

from py2neo import Graph, Node
import pandas as pd

# 连接图数据库
graph = Graph("bolt://localhost:7687/", auth=(
    'neo4j', '20040111'), name='medical')

# 提取医疗知识图谱的csv数据集文件
df = pd.read_csv('../dataset/medical.csv')
print(df.shape)    # 返回一个元组, (行数,列数)
print(df.head())   # 默认返回csv数据框的前五行，便于用户快速浏览数据(也可以在()中输入数字，指定返回的行数)

# 1.--------------------------------提取实体---------------------------------------
# 1.先试一下提取症状
# 先定义一个列表
symptoms = []
# 遍历'症状'这一列的每一个元素
for each in df['症状']:
    # 按照,分割每一个元素，并将分割后的子字符串用extend的形式，全都传给symptoms列表中
    symptoms.extend(each.split(','))
# 列表元素全部添加完成后，将列表强转为集合形式，从而去除其中的重复元素
symptoms = set(symptoms)
# print(symptoms)   # 打印所有'症状'实体

# 2.再试一下提取科室(思路同上)
departments = []
for each in df['科室']:
    departments.extend(each.split(','))
departments = set(departments)
# print(department)

# 3.检查(以下均为照抄)
checks = []
for each in df['检查']:
    checks.extend(each.split(','))
checks = set(checks)
# print(checks)

# 4.药物(有两列属性都是药物)
drugs = []
for each in df['推荐药物']:
    # 有可能无推荐药物，所以要用try,expect加以判断
    try:
        drugs.extend(each.split(','))  # 没逗号就直接追加，不用拆分了
    except:      # 如果没有药物，就直接跳过(只是保证代码健壮性罢了)
        pass
for each in df['常用药物']:
    try:
        drugs.extend(each.split(','))
    except:
        pass
drugs = set(drugs)

# 5.食物
foods = []
for each in df['可以吃']:
    try:
        foods.extend(each.split(','))
    except:
        pass
for each in df['不可以吃']:
    try:
        foods.extend(each.split(','))
    except:
        pass
for each in df['推荐吃']:
    try:
        foods.extend(each.split(','))
    except:
        pass
foods = set(foods)

# 6.所有药物厂商(具体药物中包含药物厂商)
producers = []

for each in df['具体药物']:
    try:
        for each_drug in each.split(','):
            producer = each_drug.split('(')[0]
            producers.append(producer)
    except:
        pass
producers = set(producers)

# 7.疾病字典信息
disease_infos = [] # 疾病信息
for idx, row in df.iterrows():  # 按行遍历，拿到每一行的行号idx,和每一行的数据row
    disease_infos.append(dict(row))
    # 将一行数据转化为字典形式，该行每个数据作为键值对的值，对应的列号作为键key，再追加写入disease_infos列表中
    # 即列表中的元素是字典类型，每个元素都是一个字典(且一个字典又由多个键值对组成)
    # dict()字典强转这个操作，本身就把该行row的每个元素对应的列号作为键key
dict(row).keys()   # 将键key进行返回


# 2.--------------------------------提取关系（边）------------------------------------
def deduplicate(rels_old):
    '''关系去重函数'''
    rels_new = []                   # 定义空的新列表
    for each in rels_old:           # 遍历旧列表   (含重复元素)
        if each not in rels_new:    # 如果元素不在新列表中
            rels_new.append(each)   # 那就追加写进去(如果在，就不执行任何操作)
    return rels_new                 # 返回新列表   (不含重复元素)
# 1.关系：疾病-检查
rels_check = []
for idx, row in df.iterrows():            # 按行遍历，拿到每一行的行号idx,和每一行的数据row
    # 该行的检查列对应的元素字符串有可能含逗号，切片后可能有多个子字符串each(所以需要遍历，让该行的疾病名称跟多个each组成多个二元关系)
    for each in row['检查'].split(','):
        rels_check.append([row['疾病名称'], each])
        # 将该行疾病名称和对应的检查项目组成一个二/多元关系，追加写入rels_check中
rels_check = deduplicate(rels_check)      # 对所有关系进行去重操作
# 返回的 rels_check 就是一个不含重复关系的列表，其中每个元素是形如 [疾病名称, 某个检查项目] 的二元关系
# 或者是[疾病名称, 某个检查项目1],[疾病名称, 某个检查项目2...] 的二元关系
print(rels_check)

# 2.关系：疾病-症状(后面的语法都一样，只是对应的值row['xxx']列号不一样而已)
rels_symptom = []
for idx, row in df.iterrows():
    for each in row['症状'].split(','):
        rels_symptom.append([row['疾病名称'], each])
rels_symptom = deduplicate(rels_symptom)

# 3.关系：疾病-疾病（并发症）
rels_acompany = []
for idx, row in df.iterrows():
    for each in row['并发症'].split(','):
        rels_acompany.append([row['疾病名称'], each])
rels_acompany = deduplicate(rels_acompany)

# 4.关系：疾病-推荐药物
rels_recommanddrug = []
for idx, row in df.iterrows():
    try:
        for each in row['推荐药物'].split(','):
            rels_recommanddrug.append([row['疾病名称'], each])
    except:            # 有可能该病没救了...所以没有推荐药物，遍历不了，直接pass
        pass
rels_recommanddrug = deduplicate(rels_recommanddrug)

# 5.关系：疾病-常用药物
rels_commonddrug = []
for idx, row in df.iterrows():
    try:
        for each in row['常用药物'].split(','):
            rels_commonddrug.append([row['疾病名称'], each])
    except:            # 同理没药pass
        pass
rels_commonddrug = deduplicate(rels_commonddrug)

# 6.关系：疾病-不可以吃
rels_noteat = []
for idx, row in df.iterrows():
    try:
        for each in row['不可以吃'].split(','):
            rels_noteat.append([row['疾病名称'], each])
    except:            # 吃，都可以吃！(没有不能吃的，直接pass)
        pass
rels_noteat = deduplicate(rels_noteat)

# 7.关系：疾病-可以吃
rels_doeat = []
for idx, row in df.iterrows():
    try:
        for each in row['可以吃'].split(','):
            rels_doeat.append([row['疾病名称'], each])
    except:            # 同理，都不可以吃！
        pass
rels_doeat = deduplicate(rels_doeat)

# 8.关系：疾病-推荐吃
rels_recommandeat = []
for idx, row in df.iterrows():
    try:
        for each in row['推荐吃'].split(','):
            rels_recommandeat.append([row['疾病名称'], each])
    except:             # 都不可以吃了，哪有推荐吃！
        pass
rels_recommandeat = deduplicate(rels_recommandeat)

# 9.关系：药物厂商-具体药物
rels_drug_producer = []
for each in df['具体药物']:
    try:
        for each_drug in each.split(','):
            # 根据左括号(的位置来区分生产商和药品名称
            # 1.左括号'('将字符串切分成两部分子字符串，其中索引[0]对应前面的子字符串
            producer = each_drug.split('(')[0]
            drug = each_drug.split('(')[1][:-1]
            # 2,索引[1]对应右边的子字符串，同时[:-1]操作进行切片处理，包头不包尾，选取除了末尾')'的其他子字符串内容
            rels_drug_producer.append([producer, drug])
    except:             # 无药可救...
        pass
rels_drug_producer = deduplicate(rels_drug_producer)
# 处理前:    药物厂商(具体药物)
# 处理后:    ['药物厂商','具体药物']

# 10.关系：疾病-科室、小科室-大科室
rels_category = []    # 关系：疾病-(小)科室
rels_department = []  # 关系：小科室-大科室
for idx, row in df.iterrows():
    # 如果只有一个科室，就直接"疾病-科室"的关系
    if len(row['科室'].split(',')) == 1:
        rels_category.append([row['疾病名称'], row['科室']])
    # 如果有两个科室，就先"疾病-小科室"的关系，再加一个"小科室-大科室"的关系
    else:
        big = row['科室'].split(',')[0]   # 大科室(左子字符串)
        small = row['科室'].split(',')[1] # 小科室(右子字符串)
        rels_category.append([row['疾病名称'], small])
        rels_department.append([small, big])
rels_category = deduplicate(rels_category)
rels_department = deduplicate(rels_department)

# ----------------------------neo4j数据库清空，进行初始化--------------------------------
graph.run('MATCH p=()-->() delete p')
graph.run('MATCH (n) delete n')
# 3.--------------------------------创建实体到neo4j------------------------------------
# 创造疾病实体
count = 0
# 按行遍历，每次取出列表的一行(即一个字典)
for disease_dict in disease_infos:
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
for each in drugs:
    node = Node('Drug', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
# 创建食物实体 (同理)
for each in foods:
    node = Node('Food', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
# 创建检查实体
for each in checks:
    node = Node('Check', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
# 创建科室实体
for each in departments:
    node = Node('Department', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
# 创建 药物厂商 实体
for each in producers:
    node = Node('Producer', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))
# 创建 症状 实体
for each in symptoms:
    node = Node('Symptom', name=each)
    graph.create(node)
    print('创建实体 {}'.format(each))

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
create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
# 在Disease和Food两个标签中，根据rels_recommandeat寻找能匹配上的两端节点，并进行关系创建连接
# 其中关系名为'recommand_eat',关系属性为'推荐食谱'(下面关系同理)
create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')