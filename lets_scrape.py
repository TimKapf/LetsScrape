# The main file 

import scraper
import data_helper
import visualization

kitchens = {"Asiatisch": ["Sushi", "Japanisch", "Poke bowl", "Indisch", "Thailändisch", "Curry",
                        "Vietnamesisch", "Chinesisch", "Koreanisch", "Dumplings", "Indonesisch", "Pakistanisch"],
        "Orientalisch": ["Türkisch", "Döner", "Falafel", "100% Halal", "Persisch", "Türkische Pizza",
                        "Arabisch", "Syrisch", "Libanesisch", "Gyros", "Griechisch", "Balkanküche"],
        "Italienisch": ["Italienische Pizza", "Pasta"],
        "Amerikanisch": ["Burger", "Amerikanische Pizza", "Hot Dog", "Sandwiches", "Mexikanisch", "Argentinisch", "Spareribs"],
        "Vegetarisch": ["Vegan"],
        "Cafe & Kuchen": ["Eiscreme", "Snacks", "Kuchen", "Nachspeisen", "Backwaren", "Café", "Frühstück"]}

#TODO Input of parameters
print("Hello there pls gib in welchen Modus")
print("1. einzelne Stadt")
print("2. zwei Städte")
print("3. mehr als zwei Städte")
op_1 = int(input())

if op_1 == 1:

    print("Bitte geben Sie die Stadt an.")
    city_1 = input()

elif op_1 == 2:

    print("Bitte geben Sie die erste Stadt ein")
    city_1 = input()
    print("Bitte geben Sie die zweite Stadt ein")
    city_2 = input()

elif op_1 == 3:

    citys = []

    print("Nennen Sie die Städte, die Sie vergleichen möchten getrentt mit Enter oder geben Sie 'x' zum Beenden ein")

    while('x' != input()):
        citys.append(input())
    
    print("Möchten Sie für jede Stadt einzeln die Graphen haben oder nur die Vergleichsgraphen? (true oder false)")
    op_overflow = bool(input())

else:
    print("Das war keine gültige Operation, bitte starten Sie das Programm erneut")


if op_1 < 3:
    data_1 = scraper.restaurants(city_1)
    data_2 = scraper.restaurants(city_2) if op_1 == 2 else None

if op_1 < 3 or op_overflow:
    print("Bestätigen Sie die Graphen, die Sie haben möchten mit 1 oder 0")

    """..."""



    


