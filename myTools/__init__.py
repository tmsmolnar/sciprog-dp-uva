# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# __init__.py

from .scrapingTools import scrapeBreakingBadRatings, scrapeHomelandRatings, scrapeMovieRuntime, scrapeSeriesRuntime
from .dataTools import readNetflixDataset, episodePerDay, titlePerGenre, titleType, titleTypeUnique, seriesRuntime, moviesRuntime
from .visualizationTools import watchingHabit, mostWatchedGenre, mostWatchedType, mostWatchedTypeUnique, busiestDay, heatMapBreakingBad, heatMapHomeland
