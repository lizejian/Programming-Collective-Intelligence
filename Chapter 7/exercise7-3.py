from PIL import Image, ImageDraw

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
    def __init__(self, col = -1, value = None, results = None, tb = None, fb = None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb

#在某一列上对数据集合进行拆分，能够处理数值型数据或名词型数据
def divideset(rows, column, value):
    #定义一个函数，令其告诉我们数据行属于第一组（返回值为true）还是第二组（返回值为false）
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[column] >= value
    else:
        split_function = lambda row: row[column] == value
    #将数据集拆分成两个集合，并返回
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)

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
def buildtree(rows, threshold = 0.2, scoref = entropy):
    if len(rows) == 0:
        return decisionnode()
    current_score = scoref(rows)
    #定义一些变量以记录最佳拆分条件
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    column_count = len(rows[0]) - 1
    for col in range(0, column_count):
        #在当前列中生成一个由不同值构成的序列
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1
        #接下来根据这一列中的每个值，尝试对数据集进行拆分
        for value in column_values.keys():
            set1, set2 = divideset(rows, col, value)
            #计算信息增益
            p = float(len(set1))/len(rows)
            gain = current_score - p*scoref(set1) - (1-p)*scoref(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)
    #创建子分支
    if best_gain > threshold:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return decisionnode(col = best_criteria[0], value = best_criteria[1], 
                            tb = trueBranch, fb = falseBranch)
    else:
        return decisionnode(results = uniquecounts(rows))

#以纯文本方式显示树
def printtree(tree, indent = ''):
    #这是一个叶子节点吗?
    if tree.results != None:
        print(str(tree.results))
    else:
        #打印判断条件
        print(str(tree.col) + ':' + str(tree.value) + '?')
        #打印分支
        print(indent + 'T->', end = '')#不换行
        printtree(tree.tb, indent + '  ')
        print(indent + 'F->', end = '')
        printtree(tree.fb, indent + '  ')

def classify(observation, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if v == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
    return classify(observation, branch)


if __name__ == '__main__':
    #构造决策树
    tree = buildtree(my_data)

    #纯文本
    printtree(tree)

    #对数据分类
    print(classify(['(direct)', 'USA', 'yes', 5], tree))
