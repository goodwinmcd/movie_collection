#!/usr/bin/env

from movieScrape import *

db = MySQLdb.connect('localhost','root','Ranford1', 'movieList')
c = db.cursor()
movieList = []
date = 2015
while date > 2005:
  rtUrl = 'https://www.rottentomatoes.com/top/bestofrt/?year=' + str(date)
  metaUrl = 'http://www.metacritic.com/browse/movies/score/metascore/year/filtered?year_selected=' + str(date) + '&sort=desc'
  getRTList(rtUrl, movieList)
  getMetaList(metaUrl, movieList)
  date = date - 1
f = open('fails.txt', 'w')
count = 0
movieSet = set(movieList)
print(len(movieSet))
for each in movieList:
  print(each)
  test = getIMDBURL(each)
  if test == None: f.write(each + '\n')
  inDatabase = checkDatabase(each, c)
  if inDatabase == False: 
    movie = getMovieInfo(each)
    print(movie)
    uploadMovie(movie, c)
    db.commit()   
  count = count+1
  print(count)
