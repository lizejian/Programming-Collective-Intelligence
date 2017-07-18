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

        
def kcluster(rows, distance = pearson, k = 4):
    #确定每个点的最小值和最大值
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]
    #随机创建k个中心点
    clusters = [[random.random()*(ranges[i][1] - ranges[i][0]) + ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]
    lastmatches = None
    for t in range(100):
        bestmatches = [[] for i in range(k)]
        #在每一行中寻找距离最近的中心点
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row):
                    bestmatch = i
            bestmatches[bestmatch].append(j)
        #若结果相同则结束
        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches
        #把中心点移到其所有成员的平均位置
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs
    #所有数据项彼此之间的距离总和
    totaldistance = 0.0
    for i in range(k):
        for j in range(len(bestmatches[i])):
            totaldistance += abs(distance(clusters[i], rows[bestmatches[i][j]]))
    return bestmatches, clusters, totaldistance
        
    
if __name__ == '__main__':
    #对行聚类，按照博客分类
    blognames, words, data = readfile('blogdata.txt')      
    #K-means聚类
    for K in range(3, 15):  
        kclust, clusters, distance = kcluster(data, k = K)
        print('K = ', K, '\tdistance = ', distance)    
  