# The main file 

import scraper
import data_helper
import visualization


#TODO not integrated yet
kitchens = {"Asiatisch": ["Sushi", "Japanisch", "Poke bowl", "Indisch", "Thailändisch", "Curry",
                        "Vietnamesisch", "Chinesisch", "Koreanisch", "Dumplings", "Indonesisch", "Pakistanisch"],
        "Orientalisch": ["Türkisch", "Döner", "Falafel", "100% Halal", "Persisch", "Türkische Pizza",
                        "Arabisch", "Syrisch", "Libanesisch", "Gyros", "Griechisch", "Balkanküche"],
        "Italienisch": ["Italienische Pizza", "Pasta"],
        "Amerikanisch": ["Burger", "Amerikanische Pizza", "Hot Dog", "Sandwiches", "Mexikanisch", "Argentinisch", "Spareribs"],
        "Vegetarisch": ["Vegan"],
        "Cafe & Kuchen": ["Eiscreme", "Snacks", "Kuchen", "Nachspeisen", "Backwaren", "Café", "Frühstück"]}


plots_one = ['Pie plot (Amount of kitchens)', 'Bar plot (Amount of kitchens)', 'Bar plot (Averages)']
plots_two = ['Bar plot (Amount of kitchens)', 'Bar plot (Averages)']
plots_multiple = ['3D bar plots (Amount of kitchens)', 'Heatmap (press 3 to see more)']

#TODO eine pdf oder mehrere
selected_plots_one = []
selected_plots_two = []
selected_plots_three = []

def draw_options(mode: int, number_cities: int, start_range: int=1):

    if mode == 1:
        print("Separate plots: \n")
        for plot, i in zip(plots_one, range(1, len(plots_one) + 1)):
            print(str(i) + ": " + plot + "\n")
    elif mode == 2:
        if number_cities == 2:
            print("Two city plots: \n")
            for plot, i in zip(plots_two, range(start_range, len(plots_two) + start_range)):
                print(str(i) + ": " + plot + "\n")
        elif number_cities > 2:
            print("Multiple city plots: \n")
            for plot, i in zip(plots_multiple, range(start_range, len(plots_multiple) + start_range)):
                print(str(i) + ": " + plot + "\n")
    elif mode == 3: 
        draw_options(1, number_cities)
        draw_options(2, number_cities, len(plots_one) + 1)

def avg_options() -> list:
    print("Enter \n0: All\n1: Average delivery time per kitchen\n2: Average delivery cost per kitchen\n3: Average minimum order cost per kitchen\n4: Average rating per kitchen\n")
    selections = []
    while True:
        avg = input()
        if str.lower(avg) == 'x':
            break
        elif str.lower(avg) == '0':
            selections = [1, 2, 3, 4]
            break
        selections.append(int(avg))

    return selections
        
def get_plots(mode: int, number_cities: int, selection: int, scraped_cities: list, name_cities: list, start_selection: int=1):
    if mode == 1:
        if selection == 1:
            for s_city, n_city in zip(scraped_cities, name_cities):
                selected_plots_one.append(visualization.basic_pie(s_city, n_city))
        if selection == 2:
            for s_city, n_city in zip(scraped_cities, name_cities):
                selected_plots_one.append(visualization.basic_bar(s_city, n_city))
        if selection == 3:
            selection_avg = avg_options()
            for s_city, n_city in zip(scraped_cities, name_cities):
                for avg_type in selection_avg:
                    avg_type += 1
                    selected_plots_one.append(visualization.avg_bar(s_city, avg_type, n_city)) 
    elif mode == 2:
        if number_cities == 2:
            if selection == start_selection: 
                selected_plots_two.append(visualization.kitchen_difference(scraped_cities[0], scraped_cities[1], name_cities[0], name_cities[1]))
            elif selection == start_selection + 1:
                #TODO 'Bar plot (Averages: press 3 to see more or press 4 to select same ones)' 
                selection_avg = avg_options()
                for avg_type in selection_avg:
                    avg_type += 1
                    selected_plots_two.append(visualization.avg_difference(scraped_cities[0], scraped_cities[1], name_cities[0], name_cities[1], avg_type))
        if number_cities > 2:
            if selection == start_selection:
                #TODO maybe specify kitchen 
                selected_plots_three.append(visualization.kitchen_distribution_3D(scraped_cities, name_cities))
            elif selection == start_selection + 1:
                selected_plots_three.append(visualization.heatmap(scraped_cities, name_cities))
    elif mode == 3:
        if selection < 4:
            get_plots(1, number_cities, selection, scraped_cities, name_cities) 
        else:
            get_plots(2, number_cities, selection, scraped_cities, name_cities, 4) 

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

if selection == 0:
    for s in range(1, 7):
        get_plots(decision, len(citys_scraped), s, citys_scraped, citys)
else:
    for s in selection:
        get_plots(decision, len(citys_scraped), s, citys_scraped, citys)
    
if selected_plots_one:
    visualization.get_pdf(selected_plots_one, 'plotsone.pdf')
if selected_plots_two:
    visualization.get_pdf(selected_plots_two, "plotstwo.pdf")
if selected_plots_three:
    visualization.get_pdf(selected_plots_three, "plotsmultiple.pdf")




















        







    
    



    







    


