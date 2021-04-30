# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# dataTools.py

import pandas as pd


def readDataset(filename):

    dataFrame = pd.read_excel(filename)
    #dataFrame['Date'] = pd.to_datetime(dataFrame['Date'])
    #Commented out because busiestDay() requires the original date format

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
