# Tamás Molnár
# SP - Data Processing @ UvA
# Final Project
# visualizationTools.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.palettes import Category20b_13, Category20b_14
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource, CategoricalColorMapper, HoverTool

from myTools import titlePerGenre, episodePerDay, titleType, titleTypeUnique, minutesPerTitleType, minutesPerDay, minutesPerGenre
from myTools import scrapeBreakingBadRatings, scrapeHomelandRatings


def watchingHabit(dataFrame):

    """
    Visualize the number of titles I watched based on my viewing activity dataset.

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to visualize

    Returns:
        an interactive Bokeh visualization
    """

    dataFrame = dataFrame.loc[::-1].reset_index(drop=True)

    genres = dataFrame['Genre'].unique()
    genres = list(genres)

    colorMapper = CategoricalColorMapper(
        factors=genres, palette=Category20b_13)

    source = ColumnDataSource({
        'x': dataFrame['Date'],
        'Title': dataFrame['Title'],
        'Season': dataFrame['Season'],
        'Episode_title': dataFrame['Episode title'],
        'Episode_second_title': dataFrame['Episode second title'],
        'Genre': dataFrame['Genre'],
        'Type': dataFrame['Series / Movie'],
        'index': dataFrame.index
    })

    tools = "pan, tap, box_select, lasso_select, wheel_zoom, help"
    hover = HoverTool(
        tooltips=[("Date", "@x{%F}"),
                  ("Title", "@Title"),
                  ("Season", "@Season"),
                  ("Episode title", "@Episode_title"),
                  ("Episode second title", "@Episode_second_title"),
                  ("Genre", "@Genre"),
                  ('Type', '@Type'),
                  ("Overall count", "@index")],
        formatters={'@x': 'datetime'})

    p = figure(tools=[hover, tools], plot_width=1200,
               plot_height=800, x_axis_type="datetime", y_range=(0, 1400))
    p.circle(x='x', y='index', source=source, legend_field='Genre', size=5,
             color=dict(field='Genre', transform=colorMapper))
    
    p.legend.location = 'bottom_right'
    p.title.text = 'The number of titles I watched on Netflix, since the beginning of my subscription'
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Number of titles'

    return show(p)


def mostWatchedGenre(dataFrame):

    """
    Visualize the number of titles I watched in a given genre based on my viewing activity dataset.

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to visualize

    Returns:
        a Bokeh visualization
    """

    dataFrameGenreCount = titlePerGenre(dataFrame)
    watchedGenres = list(dataFrameGenreCount.index)

    p = figure(plot_width=1200, plot_height=800,
               x_range=watchedGenres, y_range=(0, 750))
    p.vbar(x=watchedGenres, top=dataFrameGenreCount.Count,
           width=0.9, fill_color='#ed0d0e', line_alpha=0)

    p.background_fill_color = '#0b0106'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.title.text = 'My most watched genres on Netflix'
    p.xaxis.axis_label = 'Genres'
    p.yaxis.axis_label = 'Number of titles'

    return show(p)


def busiestDay(dataFrame):

    """
    Visualize on which days I watched the most titles, based on my viewing activity dataset.

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to visualize

    Returns:
        a Bokeh visualization
    """

    dataFrameDailyCounts = episodePerDay(dataFrame)
    top20Day = dataFrameDailyCounts.index[0:21]
    top20Day = list(top20Day)
    top20DayCounts = dataFrameDailyCounts['Count'][0:21]

    p = figure(plot_width=1200, plot_height=800,
               x_range=top20Day, y_range=(0, 15))
    p.vbar(x=top20Day, top=top20DayCounts, width=0.9,
           fill_color='#ed0d0e', line_alpha=0)

    p.background_fill_color = '#0b0106'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.title.text = 'The days I watched most titles on'
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Number of titles'

    return show(p)


def mostWatchedType(dataFrame):

    """
    Visualize how many title of series and movies I watched based on my viewing activity dataset.

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to visualize

    Returns:
        a Bokeh visualization
    """

    dataFrameTypeCount = titleType(dataFrame)
    watchedType = list(dataFrameTypeCount.index)

    p = figure(plot_width=1200, plot_height=800,
               x_range=watchedType, y_range=(0, 1350))
    p.vbar(x=watchedType, top=dataFrameTypeCount.Count,
           width=0.9, fill_color='#ed0d0e', line_alpha=0)
    
    p.background_fill_color = '#0b0106'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.title.text = 'The distribution of series and movies in my viewing history'
    p.xaxis.axis_label = 'Series / Movies'
    p.yaxis.axis_label = 'Number of titles'

    return show(p)


def mostWatchedTypeUnique(dataFrame):

    """
    Visualize how many unqiue title of series and movies I watched based on my viewing activity dataset.

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to visualize

    Returns:
        a Bokeh visualization
    """

    dataFrameTypeUnique = titleTypeUnique(dataFrame)

    p = figure(plot_width=1200, plot_height=800,
               x_range=dataFrameTypeUnique.Type, y_range=(0, 60))

    p.vbar(x=dataFrameTypeUnique.Type, top=dataFrameTypeUnique.Count,
           width=0.9, fill_color='#ed0d0e', line_alpha=0)

    p.background_fill_color = '#0b0106'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.title.text = 'The distribution of unique series and movies in my viewing history'
    p.xaxis.axis_label = 'Series / Movies'
    p.yaxis.axis_label = 'Number of unique titles'

    return show(p)


def heatMapBreakingBad():

    """
    Visualize Breaking Bad's episodes' ratings on a heatmap

    Parameters:
        None

    Returns:
        a Seaborn visualization
    """

    breakingBadRatings = scrapeBreakingBadRatings()
    breakingBadHeatMap = breakingBadRatings.pivot(
        "episode", "season", "userRatings")
    plt.figure(figsize=(10, 9))
    plt.title('Ratings of Breaking Bad episodes')
    ax = sns.heatmap(breakingBadHeatMap, cmap="YlGnBu", annot=True)


def heatMapHomeland():

    """
    Visualize Homeland's episodes' ratings on a heatmap

    Parameters:
        None

    Returns:
        a Seaborn visualization
    """

    homelandRatings = scrapeHomelandRatings()
    homelandHeatMap = homelandRatings.pivot("episode", "season", "userRatings")
    plt.figure(figsize=(10, 9))
    plt.title('Ratings of Homeland episodes')
    ax = sns.heatmap(homelandHeatMap, cmap="YlGnBu", annot=True)



def watchingHabitMinutes(dataFrame):

    """
    Visualize the number of minutes I watched based on my viewing activity dataset.

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to visualize

    Returns:
        an interactive Bokeh visualization
    """

    #dataFrame = dataFrame.loc[::-1].reset_index(drop=True)

    genres = dataFrame['Genre'].unique()
    genres = list(genres)
    newgenres = []

    for element in genres:
        element = str(element)
        element = element.split(' ')
        element = element[0]
        newgenres.append(element)

    colorMapper = CategoricalColorMapper(
        factors=newgenres, palette=Category20b_14)

    source = ColumnDataSource({
        'x': dataFrame['Date'],
        'Title': dataFrame['Title'],
        'Season': dataFrame['Season'],
        'Episode_title': dataFrame['Episode title'],
        'Episode_second_title': dataFrame['Episode second title'],
        'Genre': dataFrame['Genre'],
        'Type': dataFrame['Series / Movie'],
        'Runtime': dataFrame['Runtime'],
        'SpentMinutes': dataFrame['Spent Minutes'],
        'index': dataFrame.index
    })

    tools = "pan, tap, box_select, lasso_select, wheel_zoom, help"
    hover = HoverTool(
        tooltips=[("Date", "@x{%F}"),
                  ("Title", "@Title"),
                  ("Season", "@Season"),
                  ("Episode title", "@Episode_title"),
                  ("Episode second title", "@Episode_second_title"),
                  ("Genre", "@Genre"),
                  ('Type', '@Type'),
                  ('Runtime', '@Runtime'),
                  ('Overall minutes', '@SpentMinutes'),
                  ("Overall count", "@index")],
        formatters={'@x': 'datetime'})

    p = figure(tools=[hover, tools], plot_width=1200,
               plot_height=800, x_axis_type="datetime", y_range=(0,52000))
    p.circle(x='x', y='SpentMinutes', source=source, legend_field='Genre', size=5,
             color=dict(field='Genre', transform=colorMapper))

    p.legend.location = 'bottom_right'
    p.title.text = 'The number of minutes I spent watching Netflix, since the beginning of my subscription'
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Number of minutes spent'

    return show(p)

def mostWatchedGenreMinutes(dataFrame):

    """
    Visualize the number of minutes I watched in a given genre based on my viewing activity dataset and scraped information.

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to visualize

    Returns:
        an interactive Bokeh visualization
    """

    dataFrameGenreCount = minutesPerGenre(dataFrame)
    watchedGenres = list(dataFrameGenreCount.index)

    p = figure(plot_width=1200, plot_height=800,
               x_range=watchedGenres, y_range=(0, 20000))
    p.vbar(x=watchedGenres, top=dataFrameGenreCount.Count,
           width=0.9, fill_color='#ed0d0e', line_alpha=0)

    p.background_fill_color = '#0b0106'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.title.text = 'My most watched genres on Netflix'
    p.xaxis.axis_label = 'Genres'
    p.yaxis.axis_label = 'Number of minutes'

    return show(p)

def busiestDayMinutes(dataFrame):

    """
    Visualize on which days I spent the most time on Netflix based on my viewing activity dataset and scraped information

    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to visualize

    Returns:
        a Bokeh visualization
    """

    dataFrameDailyCounts = minutesPerDay(dataFrame)
    top15Day = dataFrameDailyCounts['Date'][0:16]
    top15Day = list(top15Day)
    top15DayCounts = dataFrameDailyCounts['Count'][0:16]

    p = figure(plot_width=1200, plot_height=800,
               x_range=top15Day, y_range=(0, 700))
    p.vbar(x=top15Day, top=top15DayCounts, width=0.9,
           fill_color='#ed0d0e', line_alpha=0)

    p.background_fill_color = '#0b0106'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.title.text = 'The days I watched Netflix the most'
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Number of minutes'

    return show(p)

def mostWatchedTypeMinutes(dataFrame):

    """
    Visualize the number of minutes I spent watching series and movie based on my viewing activity dataset and scraped information
    Parameters:
        dataFrame1: string
            The name of the dataFrame the user wants to visualize

    Returns:
        a Bokeh visualization
    """

    dataFrameTypeCount = minutesPerTitleType(dataFrame)
    watchedType = list(dataFrameTypeCount.index)

    p = figure(plot_width=1200, plot_height=800,
               x_range=watchedType, y_range=(0, 47000))
    p.vbar(x=watchedType, top=dataFrameTypeCount.Count,
           width=0.9, fill_color='#ed0d0e', line_alpha=0)

    p.background_fill_color = '#0b0106'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.title.text = 'How many minutes I spent watching series and movies'
    p.xaxis.axis_label = 'Series / Movies'
    p.yaxis.axis_label = 'Number of minutes'

    return show(p)
