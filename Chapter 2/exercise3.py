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
    sim_movies = []
    for movie in prefs[person1]:
        if movie in prefs[person2]:
            sim_movies.append(movie)
    if len(sim_movies) == 0:
        return 0
    total = 0
    for movie in sim_movies:
        total += (prefs[person1] - prefs[person2]) ** 2
    return 1/(1 + total ** 0.5)

#Pearson Collective Score    
def sim_pearson(prefs, person1, person2):
    #评分和
    total1, total2 = 0, 0
    #评分的平方和
    totalSq1, totalSq2 = 0, 0 
    #评分乘积和
    totalProd = 0
    sim_movies = []
    for movie in prefs[person1]:
        if movie in prefs[person2]:
            sim_movies.append(movie)
    if len(sim_movies) == 0:
        return 0
    n = len(sim_movies)
    for movie in sim_movies:
        total1 += prefs[person1][movie]
        total2 += prefs[person2][movie]
        totalSq1 += prefs[person1][movie] ** 2
        totalSq2 += prefs[person2][movie] ** 2
        totalProd += prefs[person1][movie] * prefs[person2][movie]
    num = totalProd - (total1 * total2 / n)
    den = ((totalSq1 - total1**2/n) * (totalSq2 - total2**2/n)) ** 0.5
    return num/den

#最相似的元素
def topMatches(prefs, person, similarity = sim_pearson, n = 5):
    scores = []
    for other in prefs:
        if other != person:
            sim = similarity(prefs, person, other)
            scores.append((sim, other))
    scores.sort(reverse = True)
    return scores[0:n]

#构造相似的元素集 
def calculateSimilarItems(prefs):
    sim_items = {}
    for person in prefs:
        sim_items[person] = topMatches(prefs, person)
    return sim_items
  
#main
if __name__ == '__main__':
    for person, item in calculateSimilarItems(critics).items():
        print(person, '\n', item)