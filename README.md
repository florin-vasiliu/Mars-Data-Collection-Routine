# Mission to Mars

## Objective
<img src=Mission_to_Mars/images/mission_to_mars.png>
The objective is to build a web application that scrapes various websites for data related to the Mission to Mars, and displays the information in a single HTML page.

## Project Development

The project was completed in 4 stages:

1. Development of the web scraping code where all the debugging was done in jupyter notebook (see <a href="Mission_to_Mars/mission_to_mars.ipynb">mission_to_mars.ipynb</a>)

2. OOP structuration of the scraping code and recording of results into a Mongo db (see <a href="Mission_to_Mars/scrape_mars.py">scrape_mars.py</a>) 

<img src=Mission_to_Mars/screenshots/MongoDB.PNG width=600>|
:--------------------------------------:|
MongoDB document structure|

3. Development of the flask app (see <a href="Mission_to_Mars/app.py">app.py</a>)

4. Development of the web page for rendering (see <a href="Mission_to_Mars/templates/index.html">index.html</a>). The elements of the page can be seen below:

<img src=Mission_to_Mars/screenshots/Header.PNG >|
:--------------------------------------:|
Header element: contains the latest title and the subtitle from https://mars.nasa.gov/news/, together with the "Scrape" button which triggers the updating of the page|


<img src=Mission_to_Mars/screenshots/Body1.PNG >|
:--------------------------------------:|
Body1 element: contains the weather from <a href="https://twitter.com/marswxreport?lang=en">twitter.com</a>, the mars facts from <a href="https://space-facts.com/mars/">space-facts.com</a> and the featured image from <a href="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars">jpl.nasa.gov</a>|

<img src=Mission_to_Mars/screenshots/Body2.PNG >|
:--------------------------------------:|
Body2 element: contains the Cerberus and Schiaparelli Hemispheres from <a href="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars">astrogeology.usgs.gov</a> |

<img src=Mission_to_Mars/screenshots/Body3.PNG >|
:--------------------------------------:|
Body2 element: contains the Syrtis Major and Valles Marineris Hemispheres from <a href="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars">astrogeology.usgs.gov</a> |
