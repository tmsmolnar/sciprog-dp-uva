# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# __init__.py

"""
Importing the tools coded especially for this project.

For more information about each tools:

    pydoc myTools.dataTools
    pydoc myTools.visualizationTools
    pydoc myTools.scrapingTools
    
"""

from .scrapingTools import scrapeBreakingBadRatings, scrapeHomelandRatings, scrapeMovies, scrapeSeries
from .dataTools import readNetflixDataset, episodePerDay, titlePerGenre, titleType, titleTypeUnique, seriesData, moviesData, concatSeriesMovies, cleanDataFrame, mapRuntime, mapGenre, mapType, addSpentMinutes, minutesPerDay, minutesPerGenre, minutesPerTitleType
from .visualizationTools import watchingHabit, mostWatchedGenre, mostWatchedType, mostWatchedTypeUnique, busiestDay, heatMapBreakingBad, heatMapHomeland, watchingHabitMinutes, mostWatchedGenreMinutes, busiestDayMinutes, mostWatchedTypeMinutes
