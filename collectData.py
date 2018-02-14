from omdb_API_with_python.omdbApi import find_by_id
from tmdb_API_with_python.tmdbAPI import get_movie_details_external, get_actors, \
                                         get_actor_data, get_top_rated
from webScrape.movieScrape import getRTRating, getimdbList, getRTList, \
                                  getIMDBURL, getMetaList
from pprint import pprint
from pymongo import MongoClient

def get_imdb_urls_from_rt_list(rt_list_url):
    rt_movies = getRTList(rt_list_url)
    print('returned')
    imdb_list_urls = [getIMDBURL(rt_movie) for rt_movie in rt_movies]
    print('you were wrong')
    print (imdb_list_urls)
    return imdb_list_urls, rt_movies

def get_imdb_urls_from_meta_list(meta_list_url):
    meta_movies = getMetaList(meta_list_url)
    imdb_list_urls = [getIMDBURL(meta_movie) for meta_movie in meta_movies]
    return imdb_list_urls, meta_movies

def get_imdb_urls_from_tmdb_list():
    return get_top_rated()

def check_db(imdb_id, collection):
    if imdb_id != None:
      with MongoClient() as mongo:
        db = mongo.movies
        if collection == 'movie':
            collection = db.movies
        if collection == 'actor':
            collection = db.actors
        if collection.find_one({'imdb_id' : imdb_id}) != None:
            return True
    return False

def load_movie_to_database(movie, originated = None):
    if movie != None:
      with MongoClient() as mongo:
        db = mongo.movies
        collection = db.movies
        movie_check = collection.find_one({'imdb_id' : movie['imdb_id']})
        if 'imdb_id' not in movie:
          return -1
        if check_db(movie['imdb_id'], 'movie') == False:
          collection.insert(movie)
          return 0
        else:
          if originated not in movie_check['lists']:
            movie_check['lists'].append(str(originated))
            collection.update_one({'imdb_id' : movie['imdb_id']}, {'$set': movie_check})
          return 1

def load_actor_to_database(actor, movie):
    if actor != None:
        with MongoClient() as mongo:
          db = mongo.movies
          collection = db.actors
          actor_check = collection.find_one({'imdb_id' : actor['imdb_id']})
          if 'imdb_id' not in actor:
            return -1
          if check_db(actor['imdb_id'], 'actor') == False:
            collection.insert(actor)
            return 0
          else:
            if movie not in actor_check['movies']:
                actor_check['movies'].append(str(movie))
                collection.update_one({'imdb_id' : actor['imdb_id']}, {'$set': actor_check})
            return 1

def construct_movie(imdb_id, originated = None):
    tmdb_info = get_movie_details_external(imdb_id)
    omdb_info = find_by_id(imdb_id)
    if tmdb_info == None:
        print('Could not find tmdb_info')
        return None, None
    if omdb_info == None:
        print('Could not find omdb_info')
        return None, None
    actor_list = get_actors(imdb_id)
    if actor_list != None:
        actor_list =  [get_actor_data(actor['id']) for actor in actor_list]
    else:
        actor_list = []
    for each in actor_list:
      each.pop('adult', None)
      each.pop('homepage', None)
      each.pop('also_known_as', None)
      each.pop('biography', None)
      each.pop('profile_path', None)

    rt_rating = [each['Value'] for each in omdb_info['Ratings'] if each['Source'] == 'Rotten Tomatoes']
    meta_rating = [each['Value'] for each in omdb_info['Ratings'] if each['Source'] == 'Metacritic']

    if len(rt_rating) == 0:
      rt_rating = getRTRating(tmdb_info['title'], omdb_info['Year'])
    else:
      rt_rating = int(rt_rating[0].replace('%', ''))
    list_set = set([originated])

    if omdb_info['Metascore'] != 'N/A':
      meta_rating = int(omdb_info['Metascore'])
    else:
      meta_rating = None
    imdb_rating = omdb_info['imdbRating']
    if imdb_rating != 'N/A':
        imdb_rating = int(float(omdb_info['imdbRating']) * 10)
    else:
        imdb_rating = None

    movie_asset = {
#      'actors' : [actor['id'] for actor in actor_list],
      'budget' : tmdb_info['budget'],
#      'genres_tmdb' : tmdb_info['genres'],
      'genres_omdb' : omdb_info['Genre'],
      'tmdb_id' : tmdb_info['id'],
      'imdb_id' : imdb_id,
      'original_language' : tmdb_info['original_language'],
      'tmdb_popularity' : tmdb_info['popularity'],
      'production_companies_tmdb' : tmdb_info['production_companies'],
      'country' : omdb_info['Country'],
#      'director' : omdb_info['Director'],
      'rating' : omdb_info['Rated'],
      'release_date_tmdb' : tmdb_info['release_date'],
      'release_year' : omdb_info['Year'],
      'revenue' : tmdb_info['revenue'],
      'runtime' : tmdb_info['runtime'],
#      'lists'   : list(list_set),
      'title' : tmdb_info['title'],
      'rating_imdb' : imdb_rating,
      'imdb_vote_count' : omdb_info['imdbVotes'],
      'rating_rotten_tomato' : rt_rating,
      'rating_meta' : meta_rating,
      'rating_tmdb' : int(float(tmdb_info['vote_average']) * 10),
      'tmdb_vote_count' : tmdb_info['vote_count'],
    }
    return movie_asset, actor_list

def process_error(code, movie):
    print(movie)
    if code == -1:
        with open('unsuccessful.txt', 'w') as f:
            f.write('Movie did not have imdb_id: ' + movie + '\n')
    if code == 0:
        with open('successful.txt', 'w') as f:
            f.write('Movie Successfully loaded: ' + movie+ '\n')
    if code == 1:
        with open('updated.txt', 'w') as f:
            f.write('Movie existed in db. Updated: ' + movie + '\n')

#top imdb movies
print('Retrieving imdb top movies')
imdb_titles, imdb_dates, imdb_links = getimdbList('http://www.imdb.com/chart/top?ref_=nv_mv_250_6')
print('Retrieving rotten tomatos top movies')
rt_imdb_links, rt_imdb_titles = get_imdb_urls_from_rt_list('https://www.rottentomatoes.com/top/bestofrt/')
print('Retrieving meta critic top movies')
meta_imdb_links, meta_imdb_titles = get_imdb_urls_from_meta_list('http://www.metacritic.com/browse/movies/score/metascore/90day/filtered')

with open('movies_with_None.txt', 'w') as f:
  for i, imdb_id in enumerate(imdb_links):
    if check_db(imdb_id, 'movie') == False:
        print('Processing imdb list: ' + imdb_titles[i])
        if imdb_id != None:
          movie, actors = construct_movie(imdb_id, 'imdb_top_list')
          if movie != None:
              status = load_movie_to_database(movie, 'imdb_top_list')
              process_error(status, imdb_titles[i])
              # for each in actors:
              #   each['movies'] = [movie['imdb_id']]
              #   status = load_actor_to_database(each, movie['imdb_id'])
        else:
          f.write(imdb_titles[i] + '\n')

    for i, imdb_id in enumerate(rt_imdb_links):
      if check_db(imdb_id, 'movie') == False:
          print('Processing rt list: ' + imdb_titles[i])
          if imdb_id != None:
            movie, actors = construct_movie(imdb_id, 'rt_top_list')
            if movie != None:
                status = load_movie_to_database(movie, 'rt_top_list')
                process_error(status, rt_imdb_titles[i])
                # for each in actors:
                #   each['movies'] = [movie['imdb_id']]
                #   status = load_actor_to_database(each, movie['imdb_id'])
          else:
            f.write(imdb_titles[i] + '\n')

  for i, imdb_id in enumerate(meta_imdb_links):
    if check_db(imdb_id, 'movie') == False:
        print('Processing meta list: ' + meta_imdb_titles[i])
        if imdb_id != None:
          movie, actors = construct_movie(imdb_id, 'meta_top_list')
          if movie != None:
              status = load_movie_to_database(movie, 'meta_top_list')
              process_error(status, meta_imdb_titles[i])
              # for each in actors:
              #   each['movies'] = [movie['imdb_id']]
              #   status = load_actor_to_database(each, movie['imdb_id'])
        else:
          f.write(imdb_titles[i] + '\n')
