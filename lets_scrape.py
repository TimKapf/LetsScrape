# the main file for starting the process 

import scraper
import data_refiner
import visualization

#TODO Input of parameters

#TODO Calling Scraper with desired options
a1 = "Berlin Hbf"
a2 = "Hamburg"
a3 = 'München'
a4 = 'Frankfurt'
a5 = 'Köln'
a5 = 'Osnabrück'
a6 = 'Münster'
a7 = 'Bremen'
a8 = 'Hannover'

data1 = scraper.restaurants(a1)
data2 = scraper.restaurants(a2)
data3 = scraper.restaurants(a3)
data4 = scraper.restaurants(a4)
data5 = scraper.restaurants(a5)
data6 = scraper.restaurants(a6)
data7 = scraper.restaurants(a7)
data8 = scraper.restaurants(a8)

#TODO Flatten/Refine information gathered by the scraper
#data = data_refiner.tag_correction(data)
#TODO Output of data
#a = visualization.basic_bar(data)
#b = visualization.basic_pie(data)
#visualization.discrete_distribution(data1,  ["Italienisch", "Indisch", "Sushi"])
#visualization.get_pdf([a, b])
#visualization.kitchen_difference(data1, data2, a1, a2)
#visualization.plot_3D([data1, data2], [a1, a2])
#visualization.rating_difference(data1, data2, a1, a2)
#visualization.multiple_bars_num_of_kitchens([data1, data2, data3, data4, data5], [a1, a2, a3, a4, a5])
visualization.headmap([data1, data2, data3, data4, data5, data6, data7, data8], [a1, a2, a3, a4, a5, a6, a7, a8])