import akismet

defaultkey = 'YOURKEYHER'
pageurl = 'http://yoururlhere.com'
defaultagent = 'Mozilla/5.0 (Windows; U; Windows nt 5.1; EN-us; TV:1.8.0.7)'
defaultagent += 'Gecko/20060909 Firefox/1.5.0.7'

def isspam(comment, author, ipaddress,
		agent = defaultagent,
		apikey = defaultkey):
	try:
		balid = akismet.verify_key(apikey, pageurl)
		if valid:
			return akismet.comment_check(apikey, pageurl,
				ipaddress, agent, comment_content = comment,
				comment_author_email = author, comment_type = 'comment')
		else:
			print('Invalid key')
			return False
	except akismet.akismetError, e:
		print(e.response, e.statuscode)
		return False
