# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# dataTools.py

import pandas as pd
from myTools import scrapeSeries, scrapeMovies


def readNetflixDataset(filename):

    dataFrame = pd.read_excel(filename)
    dataFrame = dataFrame.rename(columns={'Title':'Original Title'})
    dataFrame = dataFrame.join(dataFrame['Original Title'].str.split(':', expand=True).add_prefix('Original Title'))
    dataFrame = dataFrame.rename(columns={'Original Title0': 'Title'})
    dataFrame = dataFrame.rename(columns={'Original Title1': 'Season'})
    dataFrame = dataFrame.rename(columns={'Original Title2': 'Episode title'})
    dataFrame = dataFrame.rename(columns={'Original Title3': 'Episode second title'})

    return dataFrame


def episodePerDay(dataFrame):

    dataFrameDailyCounts = dataFrame['Date'].value_counts()
    dataFrameDailyCounts = dataFrameDailyCounts.to_frame()
    dataFrameDailyCounts = dataFrameDailyCounts.rename(
        columns={'Date': 'Count'})

    return dataFrameDailyCounts


def titlePerGenre(dataFrame):

    dataFrameGenreCount = dataFrame['Genre'].value_counts()
    dataFrameGenreCount = dataFrameGenreCount.to_frame()
    dataFrameGenreCount = dataFrameGenreCount.rename(
        columns={'Genre': 'Count'})

    return dataFrameGenreCount


def titleType(dataFrame):

    dataFrameTypeCount = dataFrame['Series / Movie'].value_counts()
    dataFrameTypeCount = dataFrameTypeCount.to_frame()
    dataFrameTypeCount = dataFrameTypeCount.rename(
        columns={'Series / Movie': 'Count'})

    return dataFrameTypeCount

def titleTypeUnique(dataFrame):

    dataFrameTypeUniqueSeries = dataFrame.loc[dataFrame['Series / Movie'] == 'Series']
    dataFrameTypeUniqueSeries = dataFrameTypeUniqueSeries['Title'].unique()

    dataFrameTypeUniqueMovie = dataFrame.loc[dataFrame['Series / Movie'] == 'Movie']
    dataFrameTypeUniqueMovie = dataFrameTypeUniqueMovie['Title'].unique()

    dataUniqueTitles = [['Series', len(dataFrameTypeUniqueSeries)], ['Movies', len(dataFrameTypeUniqueMovie)]]
    dataFrameTypeUniqueTitles = pd.DataFrame(dataUniqueTitles, columns=['Type', 'Count'])

    return dataFrameTypeUniqueTitles

def seriesData(dataFrame):

    onlySeries = dataFrame.loc[dataFrame['Series / Movie'] == 'Series']
    onlySeries = onlySeries['Title'].unique()
    dfOnlySeries = pd.DataFrame(data=onlySeries, columns=['Title'])

    dfSeriesData = scrapeSeries()

    newRow = pd.DataFrame({'scraped title': 'Love is Blind', 'runtime': 50,
                           'S/M': 'Series', 'genre': 'Reality-TV'}, index=[17])
    dfSeriesData = dfSeriesData.append(newRow, ignore_index=False)
    dfSeriesData = dfSeriesData.sort_index().reset_index(drop=True)

    dfSeriesData['Original Title'] = dfOnlySeries[['Title']].copy()

    dfSeriesData.loc[dfSeriesData['Original Title']
                     == 'Jeffrey Epstein', 'runtime'] = 55
    dfSeriesData.loc[dfSeriesData['Original Title']
                     == 'Lupin', 'runtime'] = 45
    dfSeriesData.loc[dfSeriesData['Original Title']
                     == "The Queen's Gambit", 'runtime'] = 55
    dfSeriesData.loc[dfSeriesData['Original Title']
                     == 'Tiger King', 'runtime'] = 45
    dfSeriesData.loc[dfSeriesData['Original Title']
                     == 'Planet Earth', 'runtime'] = 50
    dfSeriesData.loc[dfSeriesData['Original Title']
                     == 'The Blue Planet', 'runtime'] = 50
    dfSeriesData.loc[dfSeriesData['Original Title']
                     == 'Money Heist', 'runtime'] = 50

    return dfSeriesData


def moviesData(dataFrame):

    dfOnlyMovies = dataFrame.loc[dataFrame['Series / Movie'] == 'Movie']
    dfMovieData = scrapeMovies()
    dfOnlyMovies.index = dfMovieData.index
    dfMovieData['Original Title'] = dfOnlyMovies[['Original Title']].copy()

    return dfMovieData


def concatSeriesMovies(dataFrame1, dataFrame2):

    concatedDataFrame = pd.concat([dataFrame1, dataFrame2], ignore_index=True)

    return concatedDataFrame


def cleanDataFrame(dataFrame):

    cleanDataFrame = dataFrame[['Date', 'Title', 'Season', 'Episode title', 'Episode second title']]

    return cleanDataFrame


def mapRuntime(dataFrame1, dataFrame2):
    
    dataFrame1['Runtime'] = dataFrame1.Title.map(
        dataFrame2.set_index('Original Title')['runtime'].to_dict())

    return dataFrame1


def mapGenre(dataFrame1, dataFrame2):
    
    dataFrame1['Genre'] = dataFrame1.Title.map(
        dataFrame2.set_index('Original Title')['genre'].to_dict())

    return dataFrame1


def mapType(dataFrame1, dataFrame2):
    
    dataFrame1['S/M'] = dataFrame1.Title.map(
        dataFrame2.set_index('Original Title')['S/M'].to_dict())

    return dataFrame1
