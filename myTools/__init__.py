# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# __init__.py

from .dataTools import readNetflixDataset, episodePerDay, titlePerGenre, titleType
from .scrapingTools import scrapeBreakingBadRatings, scrapeHomelandRatings
from .visualizationTools import watchingHabit, mostWatchedGenre, mostWatchedType, busiestDay, heatMapBreakingBad, heatMapHomeland
