import requests
import sys
from pprint import pprint
import socket
timeout = 120
socket.setdefaulttimeout(timeout)
base_url = 'http://www.omdbapi.com/'
api_key = 'c5a65469'
default_type = 'movie'

def find_by_id(imdb_id, query_options = {'type' : default_type, 'plot' : 'full'}):
  query_string = ''
  if query_options != None:
    for each in query_options:
      query_string = '&' + each + '=' + query_options[each]
  url = base_url + '?apikey=' + api_key + '&i=' + imdb_id + query_string
  try:
    r = requests.get(url)
  except urllib.error.URLError as e:
    with open('error.log', 'w') as f:
      f.write(title + ': URLError')
  except urllib.error.HTTPError as e:
    with open('error.log', 'w') as f:
      f.write(title + ': HTTPError')
  if r.ok:
    return r.json()
  else:
    return None

def find_by_title(title, query_options = {'type' : default_type}):
  query_string = ''
  title = title.replace(' ', '+')
  if query_options != None:
    for each in query_options:
      query_string = '&' + each + '=' + query_options[each]
  url = base_url + '?apikey=' + api_key + '&t=' + title + query_string
  try:
    r = requests.get(url)
  except urllib.error.URLError as e:
    with open('error.log', 'w') as f:
      f.write(title + ': URLError')
    return None
  except urllib.error.HTTPError as e:
    with open('error.log', 'w') as f:
      f.write(title + ': HTTPError')
    return None
  except ConectionResetError as e:
    with open('error.log', 'w') as f:
      f.write(url + ': ConnectionResetErr')
    return None
  if r.ok:
    return r.json()
  else:
    return None

#pprint(findById('tt0068646'))
#pprint(find_by_title('the matrix'))
