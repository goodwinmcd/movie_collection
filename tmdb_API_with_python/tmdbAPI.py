from tmdb_API_with_python.lib.simplifiedDefinitions import elements, sort_values, actions, query_params
import requests
import sys
from pprint import pprint
import socket
timeout = 120
socket.setdefaulttimeout(timeout)
default_external = 'imdb_id'
default_element = 'movie' #defaultElement is what will be default value for all
                         #element_name function paramaters
baseUrl = 'https://api.themoviedb.org/3/'
tmdbKey = '85dd8aebef9b0ceff51463d49eaa2093'

def get_top_rated(element_name = default_element, query_options = None, num_of_movies = 100):
  movie_titles = []
  movie_imdb_urls = []
  page = 1

  while len(movie_titles) < num_of_movies:
    query_options = {'page' : page}
    url = consturct_url(action = 'top_rated', element_name = default_element,
                          query_options = query_options)
    try:
      r = requests.get(url)
    except urllib.error.URLError as e:
      with open('error.log', 'w') as f:
        f.write(url + ': URLError')
    except urllib.error.HTTPError as e:
      with open('error.log', 'w') as f:
        f.write(url + ': HTTPError')
    except ConectionResetError as e:
      with open('error.log', 'w') as f:
        f.write(url + ': ConnectionResetErr')
    for result in r.json():
      movie_titles.append(result['results']['title'])
      result_details = get_element_details(result['results']['id'])
      movie_imdb_urls = result_details['imdb_id']
    return movie_imdb_urls, movie_titles

def get_popular(element_name = default_element, query_options = None):
  url = construct_url(action = 'popular', element_name = element_name,
                     query_options = query_options)
  r = requests.get(url)
  if r.ok:
    return r.json()
  else:
    return None

def get_movie_details_external(external_id):
  tmdb_id = find_id_with_external_id(external_id)
  movie_details = get_element_details(tmdb_id)
  return movie_details


def get_element_details(element_id, element_name = default_element):
  url = construct_url(action = 'details', element_id = element_id,
                     element_name = element_name)
  r = requests.get(url)
  if r.ok:
    return r.json()
  else:
    return None

#TO-DO change this method to get actors from tmdb id instead of imdb
def get_actors(imdb_id, number_of_actors = 10):
  movie_tmdb_id = find_id_with_external_id(imdb_id)
  url = construct_url(action = 'credits', element_id = movie_tmdb_id,
    element_name = default_element)
  r = requests.get(url)
  print(r)
  print('here3')
  if r.ok:
    r = r.json()['cast'][:number_of_actors]
    return r
  else:
    return None

def get_actor_data(actor_id):
  url = construct_url(element_name = 'person', action = 'details', element_id = actor_id)
  r = requests.get(url)
  if r.ok:
    return r.json()
  else:
    return None

def find_id_with_external_id(external_id,
                      query_options = {
                        'external_source' : default_external,
                      }):
  url = construct_url(action = 'find', external_id = external_id,
                     query_options = query_options)
  r = requests.get(url)
  if r.ok and (len(r.json()['movie_results']) > 0):
    return r.json()['movie_results'][0]['id']
  else:
    return None

def get_genres(element_name = default_element):
  url = construct_url(action = 'genres', element_name = element_name)
  r = requests.get(url)
  if r.ok:
    return r.json()
  else:
    return None

def construct_url(action, element_id = None, element_name = None, external_id = None,
    query_options = None):
  check_errors(element_name = element_name, query_options = query_options)
  query_string = ''
  if query_options != None:
    for each in query_options:
      query_string = '&' + each + '=' + query_options[each]
  path = actions[action]['path'].format( element_id = element_id,
                                         element_name = element_name,
                                         external_id = external_id
  )
  url = baseUrl + path + '?api_key=' + tmdbKey + query_string
  print(url)
  return url

def check_errors(element_name = default_element, query_options = None):
  try:
    if query_options and not all(each in query_params for each in query_options):
      raise ValueError(each + ' is not a valid query param')
    if element_name and element_name not in elements:
      raise ValueError(element_name + ' is not a valid element')
  except ValueError as r:
    print(r.args[0])
    sys.exit()

#pprint(get_popular())
#pprint(get_genres())
#pprint(findWithExternalId('tt0133093'))
#pprint(find_with_external_id('tt0068646'))
#pprint(get_actors('tt0068646'))
