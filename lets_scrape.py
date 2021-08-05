# the main file for starting the process 

import scraper
import data_refiner
import visualization

#TODO Input of parameters
print("Hello dere pls gib in welchen Modus")
print("1. einzelne Stadt")
print("2. zwei Städte")
op = int(input())
if op == 1:
    print("Bitte geben Sie die Stadt ein")
    a1 = input()
else:
    print("Bitte geben Sie die erste Stadt ein")
    a1 = input()
    print("Bitte geben Sie die zweite Stadt ein")
    a2 = input()

#a1 = "Osnabrueck"
#a2 = "Berlin hbf"
data1 = scraper.restaurants(a1)
data2 = scraper.restaurants(a2) if op == 2 else None

print("Wollen Sie nur bestimmte Tags haben?(y/n)")
op2 = input()
if op2 == "y":
    print("Bitte geben Sie die Tags mit einem jeweils mit einem , und ohne Leerzeichen separiert ein")
    tags = tuple(input().split())
    data1 = data_refiner.tag_correction(restaurants=data1, w_tags=tags)
    data2 = data_refiner.tag_correction(restaurants=data2, w_tags=tags) if op == 2 else None
else:
    print("Möchten Sie bestimmte Tags ausschließen?(y/n)")
    op2 = input()
    if op2 == "y":
        print("Bitte geben Sie die Tags mit einem jeweils mit einem , und ohne Leerzeichen separiert ein")
        tags = tuple(input().split())
        data1 = data_refiner.tag_correction(restaurants=data1, uw_tags=tags)
        data2 = data_refiner.tag_correction(restaurants=data2, uw_tags=tags) if op == 2 else None

print("Data1: ", data1)
print("Data2: ", data2)
#data = data_refiner.tag_correction(data)
#TODO Output of data
#a = visualization.basic_bar(data)
#b = visualization.basic_pie(data)
#visualization.discrete_distribution(data,  ["Italienisch", "Indisch", "Sushi"])
#visualization.get_pdf([a, b])
#visualization.kitchen_difference(data1, data2, a1, a2)
