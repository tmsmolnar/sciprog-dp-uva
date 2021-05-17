# sciprog-dp-uva
Scientific Programming: Data Processing final project @ Universiteit van Amsterdam

### Data Processing - UvA

Tamás Molnár's final project for the Data Processing course at the Universiteit van Amsterdam

### Explanation

This project is based on my Netflix viewing activity, since the beginning of my subscription, until 2021-04-29

The visualizations shows the watching habit, the distribution of series and movies, the genres, the amount of minutes spent on the platform and the ratings of the episode for the chosen series

For this project, I wrote many tools and created my package to help working with data and make generalize the codes, so that it can be re-used later by anyone who needs it. The tools can be found under the myTools folder.

The original raw dataset can be found under folder datasets, alongside with a manually extended datasets that is used in the beginning of the project. The manually added information is later corrected in the notebook and visualizations with the help of the tools I created, by scraping the necessary information from iMDB, and changing the data.

For more explanation of the package see:

    pydoc myTools

    &

    pydoc myTools.dataTools
    pydoc myTools.visualizationTools
    pydoc myTools.scrapingTools



### Usage of myTools package

    from myTools import [name of the function]

### Running the assignment's notebook file

To run the Jupyter Notebook, one does not need to do anything, just click the "Run all cells" button.
However, to run this Jupyter Notebook, one needs to have the following libraries installed in advance:

    numpy, pandas, matplotlib, seaborn, bokeh, BeautifulSoup4


### Author
**2021 - Tamás Molnár - UvA**

### License
[MIT](https://choosealicense.com/licenses/mit/)
