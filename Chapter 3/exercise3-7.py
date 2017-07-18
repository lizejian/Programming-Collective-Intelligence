import random
from math import sqrt
from PIL import Image, ImageDraw

def readfile(filename):
    lines = []
    with open(filename) as f:
        lines = [line for line in f]
    #第一行是列标题
    colnames = lines[0].strip().split('\t')
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        #每行的第一列是行名
        rownames.append(p[0])
        #剩余部分是该行的数据
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data
    
def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
    num = pSum - (sum1 * sum2/len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2)/len(v1)) * (sum2Sq - pow(sum2, 2)/len(v1)))
    if den == 0:
        return 0
    return 1.0 - num/den#相似度越大的两个元素之间距离更小
    
def scaledown(data, distance = pearson, rate = 0.01):
    n = len(data)
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(n)]
    outersum = 0.0
    #随机初始化节点在一维空间中的起始位置
    loc = [random.random() for _ in range(n)]
    fakedist = [[0.0 for _ in range(n)] for _ in range(n)]
    lasterror = None
    for m in range(1000):
        #寻找投影后的距离
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = abs(loc[i] - loc[j])
        #移动节点
        grad = [0.0 for _ in range(n)]
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k:
                    continue
                #误差值等于目标距离与当前距离之间差值的百分比
                errorterm = (fakedist[j][k] - realdist[j][k])/realdist[j][k]
                #每一个节点都需要根据误差的多少，按比例移离或者移向其他节点    
                grad[k] += ((loc[k] - loc[j])/fakedist[j][k])*errorterm
                #记录总的误差值
                totalerror += abs(errorterm)
        print(totalerror)
        #如果节点移动之后的情况变得更糟，则程序结束
        if lasterror and lasterror < totalerror:
            break
        lasterror = totalerror
        #根据rate参数与grad值相乘的结果，移动每一个节点
        for k in range(n):
            loc[k] -= rate*grad[k]
    return loc
                    
def draw2d(data, labels, jpeg = 'mds2d.jpg'):
    img = Image.new('RGB', (2000, 2000), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i] + 0.5) * 1000
        draw.text((x, 1000), str(i), (0, 0, 0))
    img.save(jpeg, 'JPEG')
                    
    
if __name__ == '__main__':
    #对行聚类，按照博客分类
    blognames, words, data = readfile('blogdata.txt')
    #获得一维形式的数据集，再调用draw2d将其绘制
    coords = scaledown(data)
    draw2d(coords, blognames, jpeg = 'exercise3-7.jpg')