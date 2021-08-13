# The main file 
import scraper
import data_helper
import visualization
from ui_helper import draw_options, get_plots, avg_options, get_pdf

#TODO Handel Falscheingabe 

kitchens = {"Asiatisch": ["Sushi", "Japanisch", "Poke bowl", "Indisch", "Thailändisch", "Curry",
                        "Vietnamesisch", "Chinesisch", "Koreanisch", "Dumplings", "Indonesisch", "Pakistanisch"],
        "Orientalisch": ["Türkisch", "Döner", "Falafel", "100% Halal", "Persisch", "Türkische Pizza",
                        "Arabisch", "Syrisch", "Libanesisch", "Gyros", "Griechisch", "Balkanküche"],
        "Italienisch": ["Italienische Pizza", "Pasta"],
        "Amerikanisch": ["Burger", "Amerikanische Pizza", "Hot Dog", "Sandwiches", "Mexikanisch", "Argentinisch", "Spareribs"],
        "Vegetarisch": ["Vegan"],
        "Cafe & Kuchen": ["Eiscreme", "Snacks", "Kuchen", "Nachspeisen", "Backwaren", "Café", "Frühstück"]}

selected_plots_one = []
selected_plots_two = []
selected_plots_three = []

print("Hello. You can get plots for one, two or multiple cities.")
print("Please enter at least one adress. Type 'x' to stop. \n")
citys = []

while True:
    city = input()
    if str.lower(city) == "x":
        break
    citys.append(city)
    
# Scrape city information 
citys_scraped = []
for city in citys:
    citys_scraped.append(scraper.restaurants(city))

print("Would you like to use our custom kitchen tags (0) or the original lieferando kitchen tags (1) ?")
decision = input()
if decision == "0":
    helper = []
    for city in citys_scraped:
        helper.append(data_helper.tag_correction(city, kitchens))
    citys_scraped = helper

print("Enter 1, 2 or 3.")
if len(citys_scraped) > 2:
    print("Please select number. \n 1: Each city separately. \n 2: Plots with all cities represented. \n 3:  Separately and all cities represented.")
    decision = int(input())
 
elif len(citys_scraped) == 2:
    print("Please select number. \n 1: Each city separately. \n 2: Plots with both cities represented.  \n 3: Separately and both cities represented.")
    decision = int(input())
else:
    decision = 1

draw_options(decision, len(citys_scraped))

print("\nEnter the numbers of plots you are interested in or select 0 for all plots. Stop with 'x'.")

selection = []
while True:
    plot_type = input()
    if str.lower(plot_type) == "x":
        break
    elif str.lower(plot_type) == "0":
        selection = 0
        break
    selection.append(int(plot_type))

if selection == 0: # TODO FIX
    one_helper = {city: [] for city in citys}
    two_helper = {city: [] for city in citys}
    three_helper = {city: [] for city in citys}
    for s in range(1, 7):
        selected_plots_one, selected_plots_two, selected_plots_three = get_plots(decision, len(citys_scraped), s, citys_scraped, citys)
        if len(citys_scraped) == 1 or decision == 1 or decision == 3:
            for city in one_helper:
                one_helper[city].append(selected_plots_one[city])
        if len(citys_scraped) == 2 and (decision == 2 or decision == 3):
            for city in two_helper:
                two_helper[city].append(selected_plots_two[city])
        if len(citys_scraped) == 3 and (decision == 2 or decision == 3):
            for city in three_helper:
                three_helper[city].append(selected_plots_three[city])
        
else:
    for s in selection:
        selected_plots_one, selected_plots_two, selected_plots_three = get_plots(decision, len(citys_scraped), s, citys_scraped, citys)
    
# TODO city names richtig machen
print(selected_plots_one, selected_plots_two, selected_plots_three)

if selected_plots_one:
    for city in selected_plots_one:
        get_pdf(selected_plots_one[city], city + '.pdf')
if selected_plots_two:
    get_pdf(selected_plots_two, "plotstwo.pdf")
if selected_plots_three:
    get_pdf(selected_plots_three, "plotsmultiple.pdf")




















        







    
    



    







    


