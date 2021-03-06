import xml.dom.minidom
import requests

zwskey = 'X1-ZWz1chwxis15aj_9skq6'

def getaddressdata(address, city):
	escas = address.replace(' ', '+')
	#构造URL
	url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
  	url += 'zws-id=%s&address=%s&citystatezip=%s' % (zwskey, escad, city)
  	#解析XML形式返回的结果
  	doc = xml.dom.minidom.aprseString(requests.get(url).text)
  	code = doc.getElementsByTagName('code')[0].firstChild.data
  	#状态码为0代表操作成功，否则代表有错误发生
  	if code != '0':
  		return None
  	#提取有关该房产的信息
  	try:
  		zipcode = doc.getElementsByTagName('zipcode')[0].firstChild.data
  		use = doc.getElementsByTagName('usecode')[0].firstChild.data
  		year = doc.getElementsByTagName('yearBuilt')[0].firstChild.data
  		bath = doc.getElementsByTagName('bathrooms')[0].firstChild.data
  		bed = doc.getElementsByTagName('bedrooms')[0].firstChild.data
  		rooms = doc.getElementsByTagName('totalRooms')[0].firstChild.data
  		price = doc.getElementsByTagName('amount')[0].firstChild.data
  	except:
  		return None

  	return (zipcode, use, int(year), float(bath), int(bed), int(rooms), price)

  def getpricelist():
  	l1 = []
  	with open('addresslist.txt') as infile:
  		for line in infile:
  			data = getaddressdata(line.strip(), 'Cambridge,MA')
  			l1.append(data)
