# the main file for starting the process 

import scraper
import data_refiner
import visualization

#TODO Input of parameters

#TODO Calling Scraper with desired options
data = scraper.restaurants("Osnabrück")
#TODO Flatten/Refine information gathered by the scraper
#data = data_refiner.tag_correction(data)
#TODO Output of data
#visualization.basic_bar(data)
visualization.basic_pie(data)
#visualization.discrete_distribution(data,  ["Italienisch", "Indisch"])