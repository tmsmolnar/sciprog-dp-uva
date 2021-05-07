# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# dataTools.py

import pandas as pd
from myTools import scrapeSeriesRuntime, scrapeMovieRuntime


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

def seriesRuntime(dataFrame):

    onlySeries = dataFrame.loc[dataFrame['Series / Movie'] == 'Series']
    onlySeries = onlySeries['Title'].unique()
    dfOnlySeries = pd.DataFrame(data=onlySeries, columns=['Title'])

    dfSeriesRuntime = scrapeSeriesRuntime()

    newRow = pd.DataFrame({'title': 'Love is Blind', 'runtime': 50}, index=[17])
    dfSeriesRuntime = dfSeriesRuntime.append(newRow, ignore_index=False)
    dfSeriesRuntime = dfSeriesRuntime.sort_index().reset_index(drop=True)
    
    dfSeriesRuntime['Original Title'] = dfOnlySeries[['Title']].copy()

    dfSeriesRuntime.loc[dfSeriesRuntime['Original Title']
                    == 'Jeffrey Epstein', 'runtime'] = 55
    dfSeriesRuntime.loc[dfSeriesRuntime['Original Title']
                    == 'Lupin', 'runtime'] = 45
    dfSeriesRuntime.loc[dfSeriesRuntime['Original Title']
                    == "The Queen's Gambit", 'runtime'] = 55
    dfSeriesRuntime.loc[dfSeriesRuntime['Original Title']
                    == 'Tiger King', 'runtime'] = 45
    dfSeriesRuntime.loc[dfSeriesRuntime['Original Title']
                    == 'Planet Earth', 'runtime'] = 50
    dfSeriesRuntime.loc[dfSeriesRuntime['Original Title']
                    == 'The Blue Planet', 'runtime'] = 50
    dfSeriesRuntime.loc[dfSeriesRuntime['Original Title']
                    == 'Money Heist', 'runtime'] = 50

    return dfSeriesRuntime


def moviesRuntime(dataFrame):

    dfOnlyMovies = dataFrame.loc[dataFrame['Series / Movie'] == 'Movie']
    dfMovieRuntime = scrapeMovieRuntime()
    dfOnlyMovies.index = dfMovieRuntime.index
    dfMovieRuntime['Original Title'] = dfOnlyMovies[['Original Title']].copy()
    
    return dfMovieRuntime
