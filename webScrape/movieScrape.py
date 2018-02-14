#!/usr/bin/env

#This program defines functions that can be used to collect data on a movie from a
#given title and date.  The information is collected from imdb and also provides functions
#to retrieve the rotten tomato score and imdb score

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
logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)
timeout = 120
socket.setdefaulttimeout(timeout)
#This function retrieves a movies url on IMDB using a title and a date passed in the format of title (date)
#It will use IMDB advance search feature and show only movies within the date range of plus or minus one year.
#The movie will be found by searching for a link that has the same text as the movie titl
def getIMDBURL(title):
  logging.info('Retrieving imdb url for: ' + title)
  date = title[-5:-1]
  title = title[:-6]
  if date == '(TBA': return None
#  foreignTitle = title[title.find('(')+1:title.find(')')]	#Keeps track of the foreign title that was in parenthesis
  title = re.sub(r'\([^)]*\)', '', title)		#This removes the foreign title in parenthesis of any foreign movies
  title = title.replace(' ', '%20')
  url = 'http://www.imdb.com/search/title?adult=include&release_date=' + str(int(date)-1) + ',' + str(int(date)+1) + '&title=' + title + '&title_type=feature,short,documentary'
  url = unidecode(url)                                  #For foreign characters in movie title
  headers = {"Accept-Language":"en-US,en;q=.5"}
  try:
    req = Request(url, headers = headers)
  except urllib.error.URLError as e:
    with open('error.log', 'w') as f:
          f.write(title + ': URLError')
  except urllib.error.HTTPError as e:
    with open('error.log', 'w') as f:
          f.write(title + ': HTTPError')
  title = title.replace('%20', ' ').strip()
  page = urlopen(req)
  soup = BeautifulSoup(page, 'html.parser')
  movieLink = soup.find('a', text = title)
  if movieLink != None:
    movieLink = movieLink['href']
    movieLink = movieLink.split('/')[2]
#    movieLink = 'http://www.imdb.com' + movieLink
#  else:
#    movieLink = soup.find('a', text = foreignTitle)
#    if movieLink != None:
#      movieLink = movieLink['href']
#      movieLink = 'http://www.imdb.com' + movieLink
  return movieLink

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
  runtime = getRuntime(soup)                            #call runtime function to get runtime
  rtRating = getRTRating(title)  		        #call rtRating function to get rotten tomatos rating
  genre = getGenres(soup)                               #call genre function to get array of genres
  imdbRating = getImdbRating(soup)                      #call imdbRating function to get array of imdb rating
  metaRating = getMetaRating(soup)                      #call getMetaRating function to get meta critic rating from imdb page
  budget = getBudget(soup)                              #get budget
  gross = getRevenue(soup)                              #get revenue
  title = getTitle(soup)				#Get title	Note: The reason I rescrape the title and date is so that the date
#  title = title[:-7]
#  title = re.sub(r'\([^)]*\)', '', title)               #This removes the foreign title in parenthesis of any foreign movies
  date = getDate(soup)					#Get date	is coming from a consistent source (imdb)
  #Insert all info into a dictionary
  movieInfo = {'Title': title, 'Date': date, 'Length': runtime, 'Genres': genre, 'imdbRating': imdbRating, 'metaRating': metaRating, 'rtRating': rtRating, 'Budget': budget, 'Gross': gross,}
  return movieInfo

def getDate(soup):
  date = soup.find('span', id = 'titleYear').a.contents[0]
  return date

def getRating(soup):
  movieRating = soup.find('meta', itemprop = 'contentRating')
  if movieRating != None: movieRating = movieRating['content']
  return movieRating

def getTitle(soup):
  title = soup.find('h1', itemprop = 'name').contents[0]
  return title[:-1]

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
  c.execute("""INSERT INTO movie (title, date, runtime, budget, gross, imdb, rt, meta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", (movie['Title'], movie['Date'], movie['Length'], movie['Budget'], movie['Gross'], movie['imdbRating'], movie['rtRating'], movie['metaRating']))
  genreid = []
  #upload genres and match the corresponding genre to the correct movie id in the link table
  for each in movie['Genres']:
    c.execute("""SELECT id, descript FROM genre WHERE descript=%s;""", each)		#Check if genre is in table
    r = c.fetchall()
    if len(r) == 0:
      c.execute("""INSERT INTO genre (descript) VALUES (%s);""", (each,))		#If genre was not in table then insert the genre and
      c.execute("""SELECT * FROM genre WHERE descript=%s;""", (each,))		#keep track of the genre id
      r = c.fetchall()
      genreid.append(r[0][0])
    else:
      genreid.append(r[0][0])								#If the genre was in the table then just retrieve the id
  c.execute("""SELECT id, title FROM movie WHERE title=%s""", (movie['Title'],))	#Get the movie id
  r = c.fetchall()
  movieId = r[0][0]
  for each in genreid:								#insert the values into the linking table
    c.execute("""INSERT INTO moviegenre (movieid, genreid) VALUES (%s, %s);""", (movieId, each,))


def getBudget(soup):
  budget = soup.find('h4', text = 'Budget:')
  if budget != None:
    budget = budget.parent.contents[2].strip()
    budget = budget.replace(',','')[1:]
    budget = list(filter(str.isdigit, budget))
    budget = int(''.join(budget))
    return budget
  else: return None

def getRevenue(soup):
  gross = soup.find('h4', text = 'Gross:')
  if gross != None:
    gross = gross.parent.contents[2].strip()
    gross = gross.replace(',','')[1:]
    return int(gross)
  else: return None

def getMetaRating(soup):
  metaRating = soup.find('div', class_ = 'titleReviewBar')
  if metaRating != None:
    metaRating = metaRating.find('span').contents[0]
    metaRating = re.findall('\d+', metaRating)
    if len(metaRating) == 0: return None
    if metaRating == '\n': return None
    else: metaRating = int(metaRating[0])
  return metaRating

def getImdbRating(soup):
  imdbRating = soup.find('span', class_ = 'rating')
  if imdbRating != None: imdbRating = int(float(imdbRating.contents[0])*10)
  return imdbRating

def getGenres(soup):
  genre = soup.find_all('span', itemprop='genre')
  if genre != None:
    for i,each in enumerate(genre):
      genre[i] = genre[i].contents[0]
  return genre

def getRuntime(soup):
  runtime = soup.find('h4', text='Runtime:')
  if runtime != None:
    runtime = runtime.parent.time.contents[0]
    runtime = int(runtime.partition(' ')[0])
  if runtime == None:
    runtime = soup.find('time', itemprop = 'duration')
    if runtime != None:
      runtime = runtime['datetime']
      runtime = runtime[2:-1]
  return runtime

#RT rating was challenging because the raw html did not contain the data.  The data I needed was generated by javascript
#after the page was loaded
def getRTRating(title, date):
  title.replace(' ', '%20')
  options = Options()
  options.add_argument("--headless")
  binary = FirefoxBinary('/usr/lib/firefox/firefox')
  browser = webdriver.Firefox(firefox_options=options, firefox_binary = binary)
  url = 'https://www.rottentomatoes.com/search/?search=' + title
  try:
    browser.get(url)
  except socket.error as socketerror:
    with open('error.log', 'w') as f:
      f.write(title + ': timeout error on rt rating')
  time.sleep(1)
  html = browser.page_source
  browser.quit()
  soup = BeautifulSoup(html, 'lxml')
  results = soup.find('section', id = 'movieSection')
  if results == None: return 0
  results = results.find_all('div', class_ = 'details')
  if results == None: return 0
  #Search all returned movies on the page and only return the information if the date and title match
  for each in results:
    searchTitle = unidecode(each.span.a.contents[0])
    if searchTitle == None: return 0
    searchDate = each.find('span', class_ = 'movie_year')
    if searchDate == None: return 0
    searchDate = searchDate.contents[4]
    title = title.replace('%20', ' ')
    title = title.strip()
    #If the date plus or minus 1 of search results is within movie date AND the title matches or is within the title then it is a match
    if ((str(searchDate) == date) or (str(searchDate) == str(int(date) -1)) or (str(searchDate) == str(int(date) + 1))) and ((searchTitle.lower()) == title.lower() or (title in searchTitle)):
      rating = each.parent
      rating = rating.find('span', class_ = 'tMeterScore')
      if rating == None: return 0
      rating = rating.contents[1]
      return int(rating)
      break

#A function that collects all movie titles and dates on any specific list of imdb (like top horror movies)
def getimdbList(url):
  page = urlopen(url)
  soup = BeautifulSoup(page, "html.parser")
  titles = soup.find_all('td', class_ = 'titleColumn')
  dates = soup.find_all('span', class_ = 'secondaryInfo')
  ids = soup.find_all('div', class_ = 'wlb_ribbon')
  titleList = []
  dateList = []
  linkList = []
  for i, movies in enumerate(titles):
    titleList.append(movies.a.contents[0])
    dateList.append(str(dates[i].contents[0]))
    linkList.append(ids[i]['data-tconst']);
  return titleList, dateList, linkList


#A function that gets all movie titles and dates from any given RT list (like top 100 movies of 2016)
def getRTList(url):
  print('entered function')
  movieList = []
  page = urlopen(url)
  soup = BeautifulSoup(page, 'html.parser')
  titles = soup.find('table', class_ = 'table')
  titles = titles.find_all('a')
  print('entering for loop')
  for i, movies in enumerate(titles):
    title = str(movies.contents[0])
    title = title.strip()
    print(title)
    movieList.append(title)
  return movieList

#A function that gets all movie titles and dates from any given metacritic list (like top thrillers of all time)
def getMetaList(url):
  movieList = []
  req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
  page = urllib.request.urlopen(req)
  soup = BeautifulSoup(page, 'html.parser')
  titles = soup.find_all('div', class_ = 'title')
  dates = soup.find_all('td', class_ = 'date_wrapper')
  del titles[0]
  for i, movies in enumerate(titles):
    title = movies.a.contents[0]
    date = dates[i].span.contents[0]
    date = date.split(" ")
    date = date[len(date) - 1]
    date = "(" + date + ")"
    title = title + " " + date
    movieList.append(title)
  return movieList