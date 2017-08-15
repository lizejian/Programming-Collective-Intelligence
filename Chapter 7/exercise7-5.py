my_data = [['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]
 

class decisionnode(object):
    def __init__(self, col = -1, valuecouple = None, results = None, bn = 0, branch = None):
        self.col = col
        self.valuecouple = valuecouple
        self.results = results
        self.bn = bn
        self.branch = branch

#在某一列上对数据集合进行拆分，能够处理数值型数据或名词型数据
def divideset(rows, column, valuecouple):
    #判断有几个分类
    n = len(valuecouple)
    sets = [[] for _ in range(n + 1)]
    #定义一个函数，令其告诉我们数据行属于第一组（返回值为true）还是第二组（返回值为false）
    if isinstance(valuecouple[0], int) or isinstance(valuecouple[0], float):
        valuecouple.sort()
        for row in rows:
            if row[column] >= valuecouple[-1]:
                sets[n].append(row)
            elif row[column] < valuecouple[0]:
                sets[0].append(row)
            else:
                for i in range(n-1):
                    if valuecouple[i + 1] > row[column] >= valuecouple[i]:
                        sets[i].append(row)
    else:
        for row in rows:
            isexist = False
            for i in range(n):
                if row[column] == valuecouple[i]:
                    isexist = True
                    sets[i].append(row)
            if not isexist:
                sets[n].append(row)
    return sets

#对各种可能的结果进行计数（每一行数据的最后一列记录了这一计数结果）
def uniquecounts(rows):
    results = {}
    for row in rows:
        #计数结果在最后一列
        r = row[len(row) - 1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results

#熵是遍历所有可能的结果之后所得到的p(x)log(p(x))之和
def entropy(rows):
    from math import log
    log2 = lambda x: log(x)/log(2)
    results = uniquecounts(rows)
    #此处开始计算熵的值
    ent = 0.0
    for r in results.keys():
        p = float(results[r])/len(rows)
        ent -= p * log2(p)
    return ent

#递归函数，为当前数据集选择最合适的拆分条件来实现决策树
def buildtree(rows, scoref = entropy):
    if len(rows) == 0:
        return decisionnode()
    current_score = scoref(rows)
    #定义一些变量以记录最佳拆分条件
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(column_count):
        #在当前列中生成一个由不同值构成的序列
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1
        #所有可能的数据组合
        valuecouples = [[]]
        for value in column_values.keys():
            valuecouples += [[value] + item for item in valuecouples]
        valuecouples.pop(0)
        #接下来根据这一列中的每个值，尝试对数据集进行拆分
        for valuecouple in valuecouples:
            sets = divideset(rows, col, valuecouple)
            #计算信息增益
            new_score = 0.0
            for i in range(len(valuecouple) + 1):
                p = float(len(sets[i]))/len(rows)
                new_score += p*scoref(sets[i])
            gain = current_score - new_score
            if gain > best_gain:
                best_gain = gain
                best_criteria = (col, valuecouple)
                best_sets = sets
    #创建子分支
    if best_gain > 0:
        bn = len(best_criteria[1]) + 1
        branch = [buildtree(best_sets[i]) for i in range(bn)]
        return decisionnode(col = best_criteria[0], valuecouple = best_criteria[1], 
                            bn = bn, branch = branch)
    else:
        return decisionnode(results = uniquecounts(rows))

#以纯文本方式显示树
def printtree(tree, indent = ''):
    #这是一个叶子节点吗?
    if tree.results != None:
        print(str(tree.results))
    else:
        #打印判断条件
        print(str(tree.col) + ':' + str(tree.valuecouple) + '?')
        #打印分支
        for i in range(tree.bn):
            print(indent + '->', end = '')#不换行
            printtree(tree.branch[i], indent + '  ')

def classify(observation, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            valuecouple = tree.valuecouple.sort()
            if v >= valuecouple[-1]:
                branch = tree.branch[-1]
            elif v < valuecouple[0]:
                branch = tree.branch[0]
            else:
                for i in range(tree.bn - 1):
                    if valuecouple[i + 1] > v >= valuecouple[i]:
                        branch = tree.branch[i]
        else:
            isexist = False
            for i in range(tree.bn - 1):
                if v == tree.valuecouple[i]:    
                    isexist = True
                    branch = tree.branch[i]
            if not isexist:
                branch = tree.branch[-1]
    return classify(observation, branch)


if __name__ == '__main__':
    #构造决策树
    tree = buildtree(my_data)
    
    #显示决策树
    printtree(tree)

    #对数据分类
    print('\n', classify(['(direct)', 'USA', 'yes', 6], tree))

    