from math import sqrt
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0,
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5,
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0, 
        'Superman Returns': 3.5,
        'The Night Listener': 4.0,
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0,
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
    },
    'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0,
             'Superman Returns': 4.0},
}

#Euclidean Distance Score
def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])
    return 1/(1 + sqrt(sum_of_squares))        

#Pearson Correlation Score
def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    n = len(si)
    if n == 0:
        return 1
    #所有偏好求和
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    #平方和
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    #乘积之和
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    #计算皮尔逊评价值
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n) * (sum2Sq - pow(sum2, 2)/n))
    if den == 0:
        return 0
    r = num/den
    return r

#最佳匹配
def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    #排序
    scores.sort(reverse = True)
    return scores[0:n]

#推荐最相近的元素
def getRecommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        #不和自己比较
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        #忽略评价值为零或小于零的情况
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                #相似度*评价值
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                #相似度之和
                simSums.setdefault(item, 0)
                simSums[item] += sim
    #建立一个归一化的列表
    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    #返回经过排序的列表
    rankings.sort(reverse = True)
    return rankings

#将人员和物品对调
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            #物品和人员对调
            result[item][person] = prefs[person][item]
    return result

#构造包含相近物品的完整数据集
def calculateSimilarItems(prefs, n = 10):
    #建立字典，内容为与这些物品最为相近的其他物品
    result = {}
    #以物品为中心对偏好矩阵实施倒置处理
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        #针对大数据集更新状态变量
        c += 1
        if c % 100 == 0:
            print("%d / %d" % (c, len(itemPrefs)))
        #寻找最为相近的物品
        scores = topMatches(itemPrefs, item, n = n, similarity = sim_distance)
        result[item] = scores
    return result

#为用户推荐相近的物品    
def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    #循环遍历由当前用户评分的物品
    for (item, rating) in userRatings.items():
        #循环遍历与当前物品相近的物品
        for (similarity, item2) in itemMatch[item]:
            #如果用户已对item2做过评价，则将其忽略
            if item2 in userRatings:
                continue
            #评价值与相似度的加权之和
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            #全部相似度之和
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    #将每个合计值除以加权和，求出平均值
    rankings = [(score/totalSim[item], item) for item, score in scores.items()]
    #按最高值到最低值排序
    rankings.sort(reverse = True)
    return rankings
    
def loadMovieLens(path = 'E:/machine learing/Programming Collective Intelligence/movielens'):
    #获取影片标题
    movies = {}
    with open(path + '/u.item', 'r', encoding='gbk', errors='ignore') as f:
        try:
            for line in f:
                (id, title) = line.split('|')[0:2]
                movies[id] = title
        except:
            pass
    #加载数据
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs
    
    
if __name__ == '__main__':
    #Euclidean 
    for p1 in critics.keys():
        for p2 in critics.keys():
            if p1 != p2:
                pass
                #print(p1, ' and ', p2, 'distance:',sim_distance(critics, p1, p2))
    #Pearson
    #print('Pearson')
    for p1 in critics.keys():
        for p2 in critics.keys():
            if p1 != p2:
                pass
                #print(p1, ' and ', p2, 'distance:',sim_pearson(critics, p1, p2))
    
    #找出与Toby最匹配的人
    #print(topMatches(critics, 'Toby', 3))
    
    #为Toby推荐电影
    #print(getRecommendations(critics, 'Toby'))
    
    #将用户和电影对调
    #movies = transformPrefs(critics)
    #找出与‘Superman Returns’最匹配的电影
    #print(topMatches(movies, 'Superman Returns'))
    #为电影推荐评论者
    #print(getRecommendations(movies, 'Just My Luck'))
    
    #构造相近物品的数据集
    #itemsim = calculateSimilarItems(critics)
    #getRecommendedItems(critics, itemsim, 'Toby')
    
    #加载数据 prefs为用户评价过的电影
    prefs = loadMovieLens()
    #为用户87推荐电影，基于用户
    #getRecommendations(prefs, '87')[0:30]
    #构造相似电影的数据集
    itemsim = calculateSimilarItems(prefs, n = 50)
    #为用户87推荐电影，基于电影
    getRecommendedItems(prefs, itemsim, '87')[0:30]