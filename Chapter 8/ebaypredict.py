import http.client
from xml.dom.minidom import parse, parseString, Node

devKey = 'developerkey'
appKey = 'applicationkey'
certKey = 'certificatekey'
userToken = 'token'
serverUrl = 'api.ebay.com'

def getHeaders(apicall, siteID = '0', comptabilityLeval = '433'):
	headers = {"X-EBAY-API-COMPATIBILITY-LEVEL": compatabilityLevel, 
			"X-EBAY-API-DEV-NAME": devKey, 
			"X-EBAY-API-APP-NAME": appKey, 
			"X-EBAY-API-CERT-NAME": certKey, 
			"X-EBAY-API-CALL-NAME": apicall, 
			"X-EBAY-API-SITEID": siteID, 
			"Content-Type": "text/xml"}
	return headers

def sendRequest(apicall, xmlparameyers):
	connection = httplib.HTTPSConnection(serverUrl)
	connection.request("POST", '/ws/api.dll', xmlparameyers, getHeaders(apicall))
	response = connection.getresponse()
	if response.status != 200:
		print("Error sending request:", response.reason)
	else:
		data = response.read()
		connection.close()
	return data

def getSingleValue(node, tag):
	n1 = node.getElementsByTagName(tag)
	if len(n1) > 0:
		tagNode = n1[0]
		if tagNode.hasChildNodes():
			return tagNode.firstChild.nodeValue
	return '-1'

def doSearch(query, categoryID = None, page = 1):
	xml = "<?xml version='1.0' encoding='utf-8'?>" 
	xml += "<GetSearchResultsRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"
	xml += "<RequesterCredentials><eBayAuthToken>" 
	xml += userToken + "</eBayAuthToken></RequesterCredentials>" + "<Pagination>"
	xml += "<EntriesPerPage>200</EntriesPerPage>" + "<PageNumber>" + str(page) + "</PageNumber>"
	xml += "</Pagination>" + "<Query>" + query + "</Query>"
	if categoryID != None:
		xml += "<CategoryID>" + str(categoryID) + "</CategoryID>"
	xml += "</GetSearchResultsRequest>"
	data = sendRequest('GetSearchResults', xml)
	response = parseString(data)
	itemNodes = response.getElementsByTagName('Item')
	results = []
	for item in itemNodes:
		itemId = getSingleValue(item, 'ItmeID')
		itemTitle = getSingleValue(item, 'Title')
		itemPrice = getSingleValue(item, 'CurrentPrice')
		itemEnds = getSingleValue(item, 'EndTime')
		results.append((itemId, itemTitle, itemPrice, itemEnds))
	return results

def getCategory(query = '', parentID = None, siteID = '0'):
	lquery = query.lower()
	xml = "<GetCategoriesRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"
	xml += "<RequesterCredentials><eBayAuthToken>" + userToke
	xml += "</eBayAuthToken></RequesterCredentials>" + "<DetailLevel>ReturnAll</DetailLevel>"
	xml += "<ViewAllNodes>true</ViewAllNodes>" + "<CategorySiteID>" 
	xml += siteID + "</CategorySiteID>"
	if parentID == None:
		xml += "<LevelLimit>1</LevelLimit>"
	else:
		xml += "<CategoryParent>" + str(parentID) + "</CategoryParent>"
	xml += "</GetCategoriesRequests>"
	data = sendRequest('GetCategories', xml)
	categoryList = parseString(data)
	catNodes = categoryList.getElementsByTagName('Category')
	for node in catNodes:
		catid = getSingleValue(node, 'CategoryID')
		name = getSingleValue(node, 'CategoryName')
		if name.lower().find(lquery) != -1:
			print(catid, name)

def getItem(itemID):
  	xml = "<?xml version='1.0' encoding='utf-8'?>"
  	xml += "<GetItemRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"
  	xml += "<RequesterCredentials><eBayAuthToken>"
  	xml += userToken + "</eBayAuthToken></RequesterCredentials>"
  	xml += "<ItemID>" + str(itemID) + "</ItemID>"
  	xml += "<DetailLevel>ItemReturnAttributes</DetailLevel>" + "</GetItemRequest>"
  	data = sendRequest('GetItem', xml)
  	result = {}
  	response = parseString(data)
  	result['title'] = getSingleValue(response, 'Title')
  	sellingStatusNode = response.getElementsByTagName('SellingStatus')[0]
  	result['price'] = getSingleValue(sellingStatusNode, 'CurrentPrice')
  	result['bids'] = getSingleValue(sellingStatusNode, 'BidCount')
  	seller = response.getElementsByTagName('Seller')
  	result['feedback'] = getSingleValue(seller[0], 'FeedbackScore')
  	attributeSet = response.getElementsByTagName('Attribute')
  	attributes = []
  	for att in attributeSet:
  		attID = att.attributes.getNamedItem('attributeID').nodeValue
  		attValue = getSingleValue(att, 'ValueLiteral')
  		attributes[attID] = attValue
  	result['attributes'] = attributes
  	return results

 def makeLaptopDataset():
 	searchResults = doSearch('laptop', categoryID = 51148)
 	result = []
 	for r in searchResults:
 		item = getItem(r[0])
 		att = item['attributes']
 		try:
 			data = (float(att['12']), float(att['26444']), float(att['26446']),
 				float(att['26446']), float(att['25710']), float(item['feedback']))
 			entry = {'input':data, 'result': float(item['price'])}
 			result.append(entry)
 		except:
 			print(item['title'] + ' failed')
 		return result

 