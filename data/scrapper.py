from datetime import datetime, time, timedelta
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
perHour = 4
timenow = datetime.now()

for i in range(24*perHour):
	time_i = timenow-timedelta(hours = i/perHour+1)
	url = "https://aoe2.net/api/matches?game=aoe2de&count=1000&since="+ str(round(time_i.timestamp()) )
	r = urllib.request.urlopen(url)
	with open("matches/matches"+"%s" %i+".json", 'wb') as f:
		f.write(r.read()) 
return