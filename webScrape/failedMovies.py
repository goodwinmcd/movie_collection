#!/usr/bin/env

from movieScrape import * 

movieList = []
#rt2016 = 'https://www.rottentomatoes.com/top/bestofrt/?year=2016'
meta2016 = 'http://www.metacritic.com/browse/movies/score/metascore/year/filtered?year_selected=2016&sort=desc'
#getRTList(rt2016, movieList)
getMetaList(meta2016, movieList)
f = open('fails.txt', 'w')
count = 0
for each in movieList:
  a = getIMDBURL(each)
  if a == None:
    f.write(each + '\n')
  print(count)
  count = count + 1
