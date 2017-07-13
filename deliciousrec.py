import random
import recommandations
from pydelicious import get_popular, get_userposts, get_urlposts

def initializeUserDict(tag, count = 5):
    user_dict = {}
    #获取前count个最受欢迎的链接张贴记录
    for p1 in get_popular(tag = tag)[0: count]:
        #查找所有张贴该链接的用户
        for p2 in get_urlposts(p1['href']):
            user = p2['user']
            user_dict[user] = {}
    return user_dict

def fillItems(user_dict):
    all_items = {}
    #查找所有用户都提交过的链接
    for user in user_dict:
        for _ in range(3):
            try:
                posts = get_userposts(user)
                break
            except:
                print("Failed user ", user, ", retrying")
                time.sleep(4)
        for post in posts:
            url = post['href']
            user_dict[user][url] = 1.0
            all_items[url] = 1
        #用0填充缺失的项
        for ratings in user_dict.values():
            for item in all_items:
                if item not in ratings:
                    ratings[item] = 0.0
        
if __name__ == '__main__':
    delusers = initializeUserDict('programming')
    delusers['lizejian'] = {}
    
    #随机选择用户，找出与其品味相近的其他用户
    user = delusers.keys()[random(0, len(delusers) - 1)]
    print(recommendations.topMatches(delusers, user))
    #为该用户推荐链接
    print(recommendations.getRecommendations(delusers, user)[0:10])
    
    #获得一个链接
    url = recommendations.getRecommendations(delusers, user)[0][1]
    #与该链接最匹配的链接
    print(recommendations.topMatches(recommendations.transformPrefs(delusers), url))
    