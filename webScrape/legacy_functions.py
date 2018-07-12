from urllib.request import Request
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from unidecode import unidecode
import time
import re
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import requests
import pyvirtualdisplay
import logging
import socket

#Function to collect all movie information
#of a movie from imdb at once
def getMovieInfo(title):
  movieLink = getIMDBURL(title)
  if movieLink == None: return None
  #load movie result page
  headers = {"Accept-Language":"en-US,en;q=.5"}
  req = Request(movieLink, headers = headers)
  page = urlopen(req)
  soup = BeautifulSoup(page, 'html.parser')
  runtime = getRuntime(soup)
  rtRating = getRTRating(title)
  genre = getGenres(soup)
  imdbRating = getImdbRating(soup)
  metaRating = getMetaRating(soup)
  budget = getBudget(soup)
  gross = getRevenue(soup)
  title = getTitle(soup)
#  title = title[:-7]
   #This removes the foreign title in parenthesis of any foreign movies
#  title = re.sub(r'\([^)]*\)', '', title)
  date = getDate(soup)
  #Insert all info into a dictionary
  movieInfo = {'Title': title,
               'Date': date,
               'Length': runtime,
               'Genres': genre,
               'imdbRating': imdbRating,
               'metaRating': metaRating,
               'rtRating': rtRating,
               'Budget': budget,
               'Gross': gross,}
  return movieInfo

def checkDatabase(title, c):
  found = False
  url = getIMDBURL(title)
  if url == None: return True
  headers = {"Accept-Language":"en-US,en;q=.5"}
  req = Request(url, headers = headers)
  page = urlopen(req)
  soup = BeautifulSoup(page, 'html.parser')
  title = getTitle(soup)
  date = int(getDate(soup))
  c.execute("""SELECT title, date FROM movie WHERE title=%s""", (title,))
  r = c.fetchall()
  for each in r:
    if (each[0] == title) and (each[1] == date): found = True
  return found

#A function to upload a movie to my database
def uploadMovie(movie, c):
  c.execute("""INSERT INTO movie (title, date, runtime, budget, gross, imdb,
               rt, meta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
               (movie['Title'], movie['Date'], movie['Length'], movie['Budget'],
                movie['Gross'], movie['imdbRating'], movie['rtRating'],
                movie['metaRating']))
  genreid = []
  # upload genres and match the corresponding genre to the correct movie
  # id in the link table
  for each in movie['Genres']:
    # Check if genre is in table
    c.execute("""SELECT id, descript FROM genre WHERE descript=%s;""", each)
    r = c.fetchall()
    if len(r) == 0:
      # If genre was not in table then insert the genre and
      # keep track of the genre id
      c.execute("""INSERT INTO genre (descript) VALUES (%s);""", (each,))
      c.execute("""SELECT * FROM genre WHERE descript=%s;""", (each,))
      r = c.fetchall()
      genreid.append(r[0][0])
    else:
      # If the genre was in the table then just retrieve the id
      genreid.append(r[0][0])
  # Get the movie id
  c.execute("""SELECT id, title FROM movie WHERE title=%s""", (movie['Title'],))
  r = c.fetchall()
  movieId = r[0][0]
  # insert the values into the linking table
  for each in genreid:
    c.execute("""INSERT INTO moviegenre (movieid, genreid) VALUES (%s, %s);""",
             (movieId, each,))

def getDate(soup):
  date = soup.find('span', id = 'titleYear').a.contents[0]
  return date

def getRating(soup):
  movieRating = soup.find('meta', itemprop = 'contentRating')
  movieRating = movieRating['content'] if movieRating else return None

def getTitle(soup):
  title = soup.find('h1', itemprop = 'name').contents[0]
  return title[:-1]

def getMetaRating(soup):
  metaRating = soup.find('div', class_ = 'titleReviewBar')
  if metaRating:
    metaRating = metaRating.find('span').contents[0]
    metaRating = re.findall('\d+', metaRating)
    if len(metaRating) == 0:
      return None
    return None if metaRating == '\n' else return int(metaRating[0])
  else:
    return None

def getImdbRating(soup):
  imdbRating = soup.find('span', class_ = 'rating')
  return int(float(imdbRating.contents[0])*10) if imdbRating else return None

def getGenres(soup):
  genres = soup.find_all('span', itemprop='genre')
  return genre.contents[0] for genre in genres if genres else return None

def getRuntime(soup):
  runtime = soup.find('h4', text='Runtime:')
  if runtime:
    runtime = int(runtime.parent.time.contents[0].partition(' ')[0])
  if runtime == None:
    runtime = soup.find('time', itemprop = 'duration')
    if runtime:
      runtime = runtime['datetime'][2:-1]
  return runtime
