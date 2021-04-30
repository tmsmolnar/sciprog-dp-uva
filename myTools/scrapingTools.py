# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# scrapingTools.py

import pandas as pd
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
