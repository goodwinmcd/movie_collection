
from movieScrape import *
from urllib.request import Request
url = 'http://www.imdb.com/title/tt4016934/?ref_=nv_sr_1'
headers = {"Accept-Language":"en-US,en;q=.5"}
req = Request(url, headers = headers)
page = urlopen(req)
soup = BeautifulSoup(page, 'html.parser')
title = getTitle(soup)
print(title)
