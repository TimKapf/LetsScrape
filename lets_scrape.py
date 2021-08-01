# the main file for starting the process 

import scraper
import data_refiner
import visualization

#TODO Input of parameters

#TODO Calling Scraper with desired options
a1 = "Osnabrueck"
a2 = "Berlin hbf"
data1 = scraper.restaurants(a1)
data2 = scraper.restaurants(a2)
#TODO Flatten/Refine information gathered by the scraper
#data = data_refiner.tag_correction(data)
#TODO Output of data
#a = visualization.basic_bar(data)
#b = visualization.basic_pie(data)
#visualization.discrete_distribution(data,  ["Italienisch", "Indisch", "Sushi"])
#visualization.get_pdf([a, b])
visualization.kitchen_difference(data1, data2, a1, a2)