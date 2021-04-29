import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CategoricalColorMapper, HoverTool
from bokeh.palettes import Category20b_20
import seaborn as sns
import matplotlib.pyplot as plt


def readDataset(filename):

    dataFrame = pd.read_excel(filename)
    #dataFrame['Date'] = pd.to_datetime(dataFrame['Date'])

    return dataFrame

def episodePerDay(dataFrame):

    dataFrameDailyCounts = dataFrame['Date'].value_counts()
    dataFrameDailyCounts = dataFrameDailyCounts.to_frame()
    dataFrameDailyCounts = dataFrameDailyCounts.rename(columns={'Date': 'Count'})

    return dataFrameDailyCounts

def titlePerGenre(dataFrame):

    dataFrameGenreCount = dataFrame['Genre'].value_counts()
    dataFrameGenreCount = dataFrameGenreCount.to_frame()
    dataFrameGenreCount = dataFrameGenreCount.rename(columns={'Genre': 'Count'})

    return dataFrameGenreCount

def titleType(dataFrame):

    dataFrameTypeCount = dataFrame['Series / Movie'].value_counts()
    dataFrameTypeCount = dataFrameTypeCount.to_frame()
    dataFrameTypeCount = dataFrameTypeCount.rename(columns={'Series / Movie': 'Count'})

    return dataFrameTypeCount

def watchingHabit(dataFrame):

    dataFrame = dataFrame.loc[::-1].reset_index(drop=True)

    genres = dataFrame['Genre'].unique()
    genres = list(genres)

    colorMapper = CategoricalColorMapper(factors=genres, palette=Category20b_20)

    source = ColumnDataSource({
        'x': dataFrame['Date'],
        'Title': dataFrame['Title'],
        'Genre': dataFrame['Genre'],
        'Type': dataFrame['Series / Movie'],
        'index': dataFrame.index
    })

    tools = "pan, tap, box_select, lasso_select, wheel_zoom, help"
    hover = HoverTool(
        tooltips=[("Date", "@x{%F}"),
                ("Title", "@Title"),
                ("Genre", "@Genre"),
                ('Type', '@Type'),
                ("Overall count", "@index")],
        formatters={'@x': 'datetime'})


    p = figure(tools=[hover, tools], plot_width=1200,
            plot_height=800, x_axis_type="datetime", y_range=(0, 1400))
    p.circle(x='x', y='index', source=source, size=5,
            color=dict(field='Genre', transform=colorMapper))

    return show(p)

def mostWatchedGenre(dataFrame):

    dataFrameGenreCount = titlePerGenre(dataFrame)    
    watchedGenres = list(dataFrameGenreCount.index)

    p = figure(plot_width=1200, plot_height=800, x_range=watchedGenres, y_range=(0, 750))
    p.vbar(x=watchedGenres, top=dataFrameGenreCount.Count, width=0.9)

    return show(p)

def busiestDay(dataFrame):

    dataFrameDailyCounts = episodePerDay(dataFrame)

    top20Day = dataFrameDailyCounts.index[0:21]
    top20Day = list(top20Day)
    top20DayCounts = dataFrameDailyCounts['Count'][0:21]

    p = figure(plot_width=1200, plot_height=800, x_range=top20Day, y_range=(0,15))
    p.vbar(x=top20Day, top=top20DayCounts, width=0.9)

    return show(p)
    

def mostWatchedType(dataFrame):

    dataFrameTypeCount = titleType(dataFrame)
    
    watchedType = list(dataFrameTypeCount.index)

    p = figure(plot_width=1200, plot_height=800,
           x_range=watchedType, y_range=(0, 1350))
    p.vbar(x=watchedType, top=dataFrameTypeCount.Count, width=0.9)

    return show(p)



def scrapeBreakingBadRatings():

    breakingBadRatings = []

    for season in range(1,6):

        seasonHTML = get("https://www.imdb.com/title/tt0903747/episodes?season=" + str(season))

        pageHTML = BeautifulSoup(seasonHTML.text, 'html.parser')

        episodes = pageHTML.find_all('div', {'class':'info'} )

        for ep in episodes:
            episode = ep.meta['content']
            userRating = ep.find('span', {'class':'ipl-rating-star__rating'}).text
            data = [int(season), int(episode), float(userRating)]
            breakingBadRatings.append(data)

    dataFrame = pd.DataFrame(breakingBadRatings, columns=['season', 'episode', 'userRatings'])
    dataFrame = dataFrame.fillna(0)

    return dataFrame

def scrapeHomelandRatings():

    homelandRatings = []
    
    for season in range(1, 9):

        seasonHTML = get("https://www.imdb.com/title/tt1796960/episodes?season=" + str(season))

        pageHTML = BeautifulSoup(seasonHTML.text, 'html.parser')

        episodes = pageHTML.find_all('div', {'class': 'info'})

        for ep in episodes:
            episode = ep.meta['content']
            userRating = ep.find('span', {'class': 'ipl-rating-star__rating'}).text
            data = [int(season), int(episode), float(userRating)]
            homelandRatings.append(data)

    dataFrame = pd.DataFrame(homelandRatings, columns=['season', 'episode', 'userRatings'])
    dataFrame = dataFrame.fillna(0)

    return dataFrame

def heatMapBreakingBad():
    
    breakingBadRatings = scrapeBreakingBadRatings()
    breakingBadHeatMap = breakingBadRatings.pivot("episode", "season", "userRatings")
    plt.figure(figsize=(10, 9))
    ax = sns.heatmap(breakingBadHeatMap, cmap="YlGnBu", annot=True)

    

def heatMapHomeland():
    
    homelandRatings = scrapeHomelandRatings()
    homelandHeatMap = homelandRatings.pivot("episode", "season", "userRatings")
    plt.figure(figsize=(10, 9))
    ax = sns.heatmap(homelandHeatMap, cmap="YlGnBu", annot=True)
