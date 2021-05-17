# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# dataTools.py

import pandas as pd
from myTools import scrapeSeries, scrapeMovies


def readNetflixDataset(filename):

    """
    Load the dataset, and split the title column into title, season and episode columns.

    Parameters:
        filename: string
            The name of the file or the path of the file the user wants to load

    Returns:
        a dataFrame
    """

    dataFrame = pd.read_excel(filename)
    dataFrame = dataFrame.rename(columns={'Title':'Original Title'})
    dataFrame = dataFrame.join(dataFrame['Original Title'].str.split(':', expand=True).add_prefix('Original Title'))
    dataFrame = dataFrame.rename(columns={'Original Title0': 'Title'})
    dataFrame = dataFrame.rename(columns={'Original Title1': 'Season'})
    dataFrame = dataFrame.rename(columns={'Original Title2': 'Episode title'})
    dataFrame = dataFrame.rename(columns={'Original Title3': 'Episode second title'})

    return dataFrame


def episodePerDay(dataFrame):

    """
    Count how many times a date exists in the dataFrame.
    Used for busiestDay visualization

    Parameters:
        dataFrame: string
            The name of the dataFrame the user wants to work with.

    Returns:
        a dataFrame
    """

    dataFrameDailyCounts = dataFrame['Date'].value_counts()
    dataFrameDailyCounts = dataFrameDailyCounts.to_frame()
    dataFrameDailyCounts = dataFrameDailyCounts.rename(
        columns={'Date': 'Count'})

    return dataFrameDailyCounts


def titlePerGenre(dataFrame):

    """
    Count how many times a genre exists in the dataFrame.
    Used for mostWatchedGenre visualization

    Parameters:
        dataFrame: string
            The name of the dataFrame the user wants to work with.

    Returns:
        a dataFrame
    """

    dataFrameGenreCount = dataFrame['Genre'].value_counts()
    dataFrameGenreCount = dataFrameGenreCount.to_frame()
    dataFrameGenreCount = dataFrameGenreCount.rename(
        columns={'Genre': 'Count'})

    return dataFrameGenreCount


def titleType(dataFrame):

    """
    Count how many series and movies exists in the dataFrame.
    Used for mostWatchedType visualization

    Parameters:
        dataFrame: string
            The name of the dataFrame the user wants to work with.

    Returns:
        a dataFrame
    """

    dataFrameTypeCount = dataFrame['Series / Movie'].value_counts()
    dataFrameTypeCount = dataFrameTypeCount.to_frame()
    dataFrameTypeCount = dataFrameTypeCount.rename(
        columns={'Series / Movie': 'Count'})

    return dataFrameTypeCount

def titleTypeUnique(dataFrame):

    """
    Count how many unique series and movies exists in the dataFrame.
    Used for mostWatchedTypeUnique visualization

    Parameters:
        dataFrame: string
            The name of the dataFrame the user wants to work with.

    Returns:
        a dataFrame
    """

    dataFrameTypeUniqueSeries = dataFrame.loc[dataFrame['Series / Movie'] == 'Series']
    dataFrameTypeUniqueSeries = dataFrameTypeUniqueSeries['Title'].unique()

    dataFrameTypeUniqueMovie = dataFrame.loc[dataFrame['Series / Movie'] == 'Movie']
    dataFrameTypeUniqueMovie = dataFrameTypeUniqueMovie['Title'].unique()

    dataUniqueTitles = [['Series', len(dataFrameTypeUniqueSeries)], ['Movies', len(dataFrameTypeUniqueMovie)]]
    dataFrameTypeUniqueTitles = pd.DataFrame(dataUniqueTitles, columns=['Type', 'Count'])

    return dataFrameTypeUniqueTitles

def seriesData(dataFrame):

    """
    Create a new dataFrame containing only the series, with all the scraped informations, such as runtimes and genres.
    
    Parameters:
        dataFrame: string
            The name of the dataFrame the user wants to work with.

    Returns:
        a new dataFrame
    """

    onlySeries = dataFrame.loc[dataFrame['Series / Movie'] == 'Series']
    onlySeries = onlySeries['Title'].unique()
    dfOnlySeries = pd.DataFrame(data=onlySeries, columns=['Title'])

    dfSeriesData = scrapeSeries()

    newRow = pd.DataFrame({'scraped title': 'Love is Blind', 'runtime': 50,
                           'S/M': 'Series', 'genre': 'Reality-TV'}, index=[17])
    dfSeriesData = dfSeriesData.append(newRow, ignore_index=False)
    dfSeriesData = dfSeriesData.sort_index().reset_index(drop=True)

    dfSeriesData['Title'] = dfOnlySeries[['Title']].copy()

    dfSeriesData.loc[dfSeriesData['Title']
                     == 'Jeffrey Epstein', 'runtime'] = 55
    dfSeriesData.loc[dfSeriesData['Title']
                     == 'Lupin', 'runtime'] = 45
    dfSeriesData.loc[dfSeriesData['Title']
                     == "The Queen's Gambit", 'runtime'] = 55
    dfSeriesData.loc[dfSeriesData['Title']
                     == 'Tiger King', 'runtime'] = 45
    dfSeriesData.loc[dfSeriesData['Title']
                     == 'Planet Earth', 'runtime'] = 50
    dfSeriesData.loc[dfSeriesData['Title']
                     == 'The Blue Planet', 'runtime'] = 50
    dfSeriesData.loc[dfSeriesData['Title']
                     == 'Money Heist', 'runtime'] = 50

    return dfSeriesData


def moviesData(dataFrame):

    """
    Create a new dataFrame containing only the movies, with all the scraped informations, such as runtimes and genres.
    
    Parameters:
        dataFrame: string
            The name of the dataFrame the user wants to work with.

    Returns:
        a new dataFrame
    """

    dfOnlyMovies = dataFrame.loc[dataFrame['Series / Movie'] == 'Movie']
    dfMovieData = scrapeMovies()
    dfOnlyMovies.index = dfMovieData.index
    dfMovieData['Original Title'] = dfOnlyMovies[['Original Title']].copy()

    list_to_column = []


    for i in dfMovieData['Original Title']:
        i = i.split(':')
        i = i[0]
        list_to_column.append(i)

    dfMovieData['Title'] = list_to_column

    return dfMovieData


def concatSeriesMovies(dataFrame1, dataFrame2):

    """
    Join, concat two dataFrames
    
    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to concat.
        dataFrame2: string
            The name of the dataFrame the user wants to concat.

    Returns:
        a new dataFrame
    """

    concatedDataFrame = pd.concat([dataFrame1, dataFrame2], ignore_index=True)

    return concatedDataFrame


def cleanDataFrame(dataFrame):

    """
    Clean a dataFrame and use only the necessary columns for the visualizations.
    
    Parameters:
        dataFrame: string
            The name of the dataFrame the user wants to work with.

    Returns:
        a dataFrame
    """

    cleanDataFrame = dataFrame[['Original Title', 'Date', 'Title', 'Season', 'Episode title', 'Episode second title']]

    return cleanDataFrame


def mapRuntime(dataFrame1, dataFrame2):

    """
    Add the scraped runtimes of the titles in the viewing activity dataframe
    
    Parameters:
        dataFrame1: string
            The name of the dataFrame to which the user wants to add the runtime
        dataFrame2: string
            The name of the dataFrame containging the runtimes.

    Returns:
        a dataFrame
    """

    dataFrame1['Runtime'] = dataFrame1.Title.map(
        dataFrame2.set_index('Title')['runtime'].to_dict())

    return dataFrame1


def mapGenre(dataFrame1, dataFrame2):

    """
    Add the scraped genres of the titles in the viewing activity dataframe

    Parameters:
        dataFrame1: string
            The name of the dataFrame to which the user wants to add the genres
        dataFrame2: string
            The name of the dataFrame containging the genres.

    Returns:
        a dataFrame
    """

    dataFrame1['Genre'] = dataFrame1.Title.map(
        dataFrame2.set_index('Title')['genre'].to_dict())

    return dataFrame1


def mapType(dataFrame1, dataFrame2):

    """
    Add the "scraped" type of the titles in the viewing activity dataframe

    Parameters:
        dataFrame1: string
            The name of the dataFrame to which the user wants to add the type of the title
        dataFrame2: string
            The name of the dataFrame containging the types.

    Returns:
        a dataFrame
    """

    dataFrame1['S/M'] = dataFrame1.Title.map(
        dataFrame2.set_index('Title')['S/M'].to_dict())

    return dataFrame1


def addSpentMinutes(dataFrame):

    """
    Create a new column with the amount of spent minutes on Netflix, by adding the current row's runtime's value to the column

    Parameters:
        dataFrame1: string
            The name of the dataFrame in which the user wants to calculate the spent minutes

    Returns:
        a dataFrame
    """

    dataFrame = dataFrame.rename(columns={'S/M': 'Series / Movie'})
    dataFrame['Spent Minutes'] = 0
    dataFrame = dataFrame.loc[::-1].reset_index(drop=True)

    for i in range(1, len(dataFrame)):
        dataFrame.loc[i, 'Spent Minutes'] = dataFrame.loc[i, 'Runtime'] + dataFrame.loc[i-1, 'Spent Minutes']

    return dataFrame


def minutesPerDay(dataFrame):

    """
    Calculate the number of minutes spent on Netflix each day
    Used for busiestDayMinutes visualization

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to work with

    Returns:
        a dataFrame
    """

    dataFrame = dataFrame.groupby('Date')['Runtime'].sum()
    dataFrame = dataFrame.to_frame()
    dataFrame['Date'] = dataFrame.index
    dataFrame['Date'] = dataFrame['Date'].dt.strftime('%m/%d/%Y')
    dataFrame = dataFrame.rename(
        columns={'Runtime': 'Count'})
    dataFrame = dataFrame.sort_values(by='Count',ascending=False)

    return dataFrame

def minutesPerGenre(dataFrame):

    """
    Calculate the number of minutes spent by watching each genre
    Used for mostWatchedGenreMinutes visualization

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to work with

    Returns:
        a dataFrame
    """

    dataFrame = dataFrame.join(dataFrame['Genre'].str.split(' ', expand=True).add_prefix('Genre clean'))
    dataFrame = dataFrame.groupby('Genre clean0')['Runtime'].sum()
    dataFrame = dataFrame.to_frame()
    dataFrame = dataFrame.rename(
        columns={'Runtime': 'Count'})
    dataFrame = dataFrame.sort_values(by='Count', ascending=False)

    return dataFrame

def minutesPerTitleType(dataFrame):

    """
    Calculate the number of minutes spent watching title types.
    Used for mostWatchedTypeMinutes visualization

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to work with

    Returns:
        a dataFrame
    """

    dataFrame = dataFrame.groupby('Series / Movie')['Runtime'].sum()
    dataFrame = dataFrame.to_frame()
    dataFrame = dataFrame.rename(
        columns={'Runtime': 'Count'})
    dataFrame = dataFrame.sort_values(by='Count', ascending=False)

    return dataFrame

