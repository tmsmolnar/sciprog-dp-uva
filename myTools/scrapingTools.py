# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# scrapingTools.py

import pandas as pd
import requests
from requests import get
from bs4 import BeautifulSoup


def scrapeBreakingBadRatings():

    breakingBadRatings = []

    for season in range(1, 6):
        seasonHTML = get(
            "https://www.imdb.com/title/tt0903747/episodes?season=" + str(season))
        pageHTML = BeautifulSoup(seasonHTML.text, 'html.parser')
        episodes = pageHTML.find_all('div', {'class': 'info'})

        for ep in episodes:
            episode = ep.meta['content']
            userRating = ep.find(
                'span', {'class': 'ipl-rating-star__rating'}).text
            data = [int(season), int(episode), float(userRating)]
            breakingBadRatings.append(data)

    dataFrame = pd.DataFrame(breakingBadRatings, columns=[
                             'season', 'episode', 'userRatings'])
    dataFrame = dataFrame.fillna(0)

    return dataFrame


def scrapeHomelandRatings():

    homelandRatings = []

    for season in range(1, 9):
        seasonHTML = get(
            "https://www.imdb.com/title/tt1796960/episodes?season=" + str(season))
        pageHTML = BeautifulSoup(seasonHTML.text, 'html.parser')
        episodes = pageHTML.find_all('div', {'class': 'info'})

        for ep in episodes:
            episode = ep.meta['content']
            userRating = ep.find(
                'span', {'class': 'ipl-rating-star__rating'}).text
            data = [int(season), int(episode), float(userRating)]
            homelandRatings.append(data)

    dataFrame = pd.DataFrame(homelandRatings, columns=[
                             'season', 'episode', 'userRatings'])
    dataFrame = dataFrame.fillna(0)

    return dataFrame


def scrapeMovies():

    moviesData = []

    moviesHTML = 'https://www.imdb.com/list/ls500759439/'
    response = requests.get(moviesHTML)
    html = response.content
    pageHTML = BeautifulSoup(html, 'html.parser')
    
    movies = pageHTML.find_all('div', {'class':'lister-item mode-detail'})

    for movie in movies:

        title = movie.find('h3', {'class': 'lister-item-header'})
        title = title.text.split("\n")
        
        runtime = movie.find('span', {'class': 'runtime'})
        runtime = runtime.text.split(" min")

        genre = movie.find('span', {'class':'genre'})
        genre = genre.text.split(",")
        genre = genre[0].split("\n")

        data = [str(title[2]), int(runtime[0]), str(genre[1]), 'Movie']

        moviesData.append(data)

    dataFrame = pd.DataFrame(moviesData, columns=[
        'scraped title', 'runtime', 'genre', 'S/M'])
    dataFrame = dataFrame.fillna(0)

    return dataFrame


def scrapeSeries():

    seriesData = []

    seriesHTML = 'https://www.imdb.com/list/ls500780679/'
    response = requests.get(seriesHTML)
    html = response.content
    pageHTML = BeautifulSoup(html, 'html.parser')

    series = pageHTML.find_all('div', {'class': 'lister-item mode-detail'})

    for s in series:

        title = s.find('h3', {'class': 'lister-item-header'})
        title = title.text.split("\n")

        runtime = s.find('span', {'class': 'runtime'})
        runtime = runtime.text.split(" min")

        genre = s.find('span', {'class': 'genre'})
        genre = genre.text.split(",")
        genre = genre[0].split("\n")

        data = [str(title[2]), int(runtime[0]), str(genre[1]), 'Series']

        seriesData.append(data)

    dataFrame = pd.DataFrame(seriesData, columns=[
        'scraped title', 'runtime', 'genre', 'S/M'])
    dataFrame = dataFrame.fillna(0)

    return dataFrame
            

