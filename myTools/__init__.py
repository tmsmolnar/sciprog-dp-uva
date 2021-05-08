# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# __init__.py

from .scrapingTools import scrapeBreakingBadRatings, scrapeHomelandRatings, scrapeMovies, scrapeSeries
from .dataTools import readNetflixDataset, episodePerDay, titlePerGenre, titleType, titleTypeUnique, seriesData, moviesData
from .visualizationTools import watchingHabit, mostWatchedGenre, mostWatchedType, mostWatchedTypeUnique, busiestDay, heatMapBreakingBad, heatMapHomeland
