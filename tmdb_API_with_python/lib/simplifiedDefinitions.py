

actions =  {
  'airing_today' : {
    'path' : '{element_name}/{element_id}',
  },
  'alternative_titles' : {
    'path' : '{element_name}/{element_id}/alternative_titles',
  },
  'changes' : {
    'path' : '{element_name}/changes',
  },
  'combined_credits' : {
    'path' : '{element_name}/{element_id}/combined_credits',
  },
  'content_ratings' : {
    'path' : '{element_name}/{element_id}/content_ratings',
  },
  'credits' : {
    'path' : '{element_name}/{element_id}/credits',
  },
  'details' : {
    'path' : '{element_name}/{element_id}',
  },
  'discover' : {
    'path' : 'discover/{element_name}',
  },
  'external_ids' : {
    'path' : '{element_name}/{element_id}/external_ids',
  },
  'find' : {
    'path' : 'find/{external_id}',
  },
  'genres' : {
    'path' : 'genre/{element_name}/list',
  },
  'images' : {
    'path' : '{element_name}/{element_id}/images',
  },
  'jobs' : {
    'path' : 'job/list',
  },
  'keywords' : {
    'path' : '{element_name}/{element_id}/keywords',
  },
  'latest' : {
    'path' : '{element_name}/latest',
  },
  'lists' : {
    'path' : '{element_name}/{element_id}/lists',
  },
  # 'movies' : {
  #   'descript' : '''Returns movies associated to a specific element_id''',
  #   'path' : 'movie/',
  #   'elig_elements' : [
  #     'company',
  #   ],
  #   'requires' : [
  #     'element_name',
  #     'element_id',
  #   ],
  # },
  'movie_credits' : {
    'path' : '{element_name}/{element_id}/movie_credits',
  },
  'now_playing' : {
    'path' : '{element_name}/now_playing',
  },
  'on_the_air' : {
    'path' : '{element_name}/on_the_air',
  },
  'popular' : {
    'path' : '{element_name}/popular',
  },
  'recommendations' : {
    'path' : '{element_name}/{element_id}/recomendations',
  },
  'release_dates' : {
    'path' : '{element_name}/{element_id}/release_dates',
  },
  'reviews' : {
    'path' : '{element_name}/{element_id}/reviews',
  },
  'search' : {
    'path' : 'search/{element_name}',
  },
  'screened_theatrically' : {
    'path' : '{element_name}/{element_id}/screened_theatrically',
  },
  'search_multi' : {
    'path' : 'search/multi/',
  },
  'similar' : {
    'path' : '{element_name}/{element_id}/similar',
  },
  'tagged_images' : {
    'path' : '{element_name}/{element_id}/tagged_images',
  },
  'top_rated' : {
    'path' : '{element_name}/top_rated',
  },
  'translations' : {
    'path' : '{element_name}/{element_id}/translations',
  },
  'tv_credits' : {
    'path' : '{element_name}/{element_id}/tv_credits',
  },
  'upcoming' : {
    'path' : '{element_name}/upcoming',
  },
  'videos' : {
    'path' : '{element_name}/{element_id}/videos',
  },
}

query_params = {
  'api_key' : {
    'related_actions' : [
      'airing_today',
      'alternative_titles',
      'changes',
      'collection',
      'combined_credits',
      'content_ratings',
      'credits',
      'details',
      'discover',
      'external_ids',
      'find',
      'images',
      'jobs',
      'keywords',
      'latest',
      'lists',
      'movies',
      'movie_credits',
      'networks',
      'now_playing',
      'on_the_air',
      'popular',
      'recommendations',
      'release_dates',
      'reviews',
      'screened_theatrically',
      'search',
      'similar',
      'tagged_images',
      'top_rated',
      'translations',
      'tv_credits',
      'upcoming',
      'videos',
    ],
  },
  'air_date.gte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'air_date.lte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'append_to_response' : {
    'related_actions' : [
      'details',
    ],
  },
  'certification' : {
    'related_actions' : [
      'discover',
    ],
  },
  'certification.lte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'certification_country' : {
    'related_actions' : [
      'discover',
    ],
  },
  'country' : {
    'related_actions' : [
      'alternative_titles',
    ],
  },
  'end_date' : {
    'related_actions' : [
      'changes',
    ],
  },
  'external_source' : {
    'related_actions' : [
      'find/',
    ],
  },
  'first_air_date' : {
    'related_actions' : [
      'search',
    ],
  },
  'first_air_date.gte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'first_air_date.lte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'include_adult' : {
    'related_actions' : [
      'discover',
      'genres',
      'keywords',
      'search',
    ],
  },
  'include_null_first_air_dates' : {
    'related_actions' : [
      'discover',
    ],
  },
  'include_video' : {
    'related_actions' : [
      'discover',
    ],
  },
  'include_image_language' : {
    'related_actions' : [
      'images',
    ],
  },
  'language' : {
    'related_actions' : [
      'airing_today',
      'collection',
      'combined_credits',
      'content_ratings',
      'details',
      'discover',
      'external_ids',
      'find',
      'images',
      'genres',
      'keywords',
      'latest',
      'lists',
      'movies',
      'movie_credits',
      'on_the_air',
      'popular',
      'search',
      'recommendations',
      'reviews',
      'similar',
      'tagged_images',
      'top_rated',
      'translations',
      'tv_credits',
      'upcoming',
      'videos',
    ],
  },
  'page' : {
    'related_actions': [
      'airing_today',
      'changes',
      'discover',
      'lists',
      'now_playing',
      'on_the_air',
      'popular',
      'reviews',
      'search',
      'similar',
      'tagged_images',
      'top_rated',
      'upcoming',
    ],
  },
  'primary_release_year' : {
    'related_actions' : [
      'discover',
    ],
  },
  'primary_release_year.gte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'primary_release_year.lte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'query' : {
    'related_actions' : [
      'search',
    ],
  },
  'region' : {
    'related_actions' : [
      'discover',
      'now_playing',
      'popular',
      'search',
      'top_rated',
      'upcoming',
    ],
  },
  'release_date.gte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'release_date.lte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'screened_theatrically' : {
    'related_actions' : [
      'discover',
    ],
  },
  'sort_by' : {
    'related_actions' : [
      'discover',
      'genres',
    ],
  },
  'start_date' : {
    'related_actions' : [
      'changes',
    ],
  },
  'vote_average.gte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'vote_average.lte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'vote_count.gte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'vote_count.lte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_cast' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_companies' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_crew' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_genres' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_keywords' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_networks' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_original_language' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_people' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_release_type' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_runtime.gte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'with_runtime.lte' : {
    'related_actions' : [
      'discover',
    ],
  },
  'without_genres' : {
    'related_actions' : [
      'discover',
    ],
  },
  'without_keywords' : {
    'related_actions' : [
      'discover',
    ],
  },
  'year' : {
    'related_actions' : [
      'discover',
    ],
  },
}

elements = {
  'collection' : 'collection',
  'company' : 'company',
  'credits' : 'credits',
  'genre' : 'genre',
  'keyword' : 'keyword',
  'movie' : 'movie',
  'networks' : 'network',
  'person' : 'person',
  'review' : 'review',
  'tv' : 'tv',
}

sort_values = {
  'popularity.asc',
  'popularity.desc',
  'release_date.asc',
  'release_date.desc',
  'revenue.asc',
  'revenue.desc',
  'primary_release_date.asc',
  'primary_release_date.desc',
  'original_title.asc',
  'original_title.desc',
  'vote_average.asc',
  'vote_average.desc',
  'vote_count.asc',
  'vote_count.desc'
  #default: popularity.desc
}
