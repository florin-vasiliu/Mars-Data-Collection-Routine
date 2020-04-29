# Web Scraping Challenge

This project was completed in 3 stages:

1. Development of the web scraping code where all the debugging was done in jupyter notebook (see "mission_to_mars.ipynb")
2. OOP structuration of the scraping code (see "scrape_mars.py") and development of the flask app (see "app.py")
3. Development of the web page for rendering (see "index.html"). The elements of the page can be seen below:

<img src=Mission_to_Mars/screenshots/Header.PNG >|
:--------------------------------------:|
Header element: contains the latest title and the subtitle from https://mars.nasa.gov/news/|


<img src=Mission_to_Mars/screenshots/Body1.PNG >|
:--------------------------------------:|
Body1 element: contains the weather from <a href="https://twitter.com/marswxreport?lang=en">twitter.com</a>, the mars facts from <a href="https://space-facts.com/mars/">space-facts.com</a> and the featured image from <a href="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars">jpl.nasa.gov</a>|

<img src=Mission_to_Mars/screenshots/Body2.PNG >|
:--------------------------------------:|
Body2 element: contains the Cerberus and Schiaparelli Hemispheres from <a href="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars">astrogeology.usgs.gov</a> |

<img src=Mission_to_Mars/screenshots/Body3.PNG >|
:--------------------------------------:|
Body2 element: contains the Syrtis Major and Valles Marineris Hemispheres from <a href="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars">astrogeology.usgs.gov</a> |
