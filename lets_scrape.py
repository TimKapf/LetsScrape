# The main file 
import scraper
import data_helper
import visualization
from ui_helper import draw_options, get_plots, avg_options, get_pdf

# categories for custom kitchen tags
kitchens = {"Asiatisch": ["Asiatisch", "Sushi", "Japanisch", "Poke bowl", "Indisch", "Thailändisch", "Curry",
                        "Vietnamesisch", "Chinesisch", "Koreanisch", "Dumplings", "Indonesisch", "Pakistanisch"],
        "Orientalisch": ["Orientalisch", "Türkisch", "Döner", "Falafel", "100% Halal", "Persisch", "Türkische Pizza",
                        "Arabisch", "Syrisch", "Libanesisch", "Gyros", "Griechisch", "Balkanküche"],
        "Italienisch": ["Italienisch", "Italienische Pizza", "Pasta"],
        "Amerikanisch": ["Amerikanisch", "Burger", "Amerikanische Pizza", "Hot Dog", "Sandwiches", "Mexikanisch", "Argentinisch", "Spareribs"],
        "Vegetarisch": ["Vegetarisch", "Vegan"],
        "Cafe & Kuchen": ["Eiscreme", "Snacks", "Kuchen", "Nachspeisen", "Backwaren", "Café", "Frühstück"]}

selected_plots_one = []
selected_plots_two = []
selected_plots_three = []

# Ask for adresses
print("Hello. You can get plots for one, two or multiple cities.")
print("Please enter at least one adress. Type 'x' to stop. \n")
citys = []

# Input of adresses, stop if the input is x
while True:
    city = input()
    if str.lower(city) == "x":
        break
    citys.append(city)
    
# Scrape city information 
citys_scraped = []
for city in citys:
    citys_scraped.append(scraper.restaurants(city))

# Ask which kitchen categories to use
print("Would you like to use our custom kitchen tags (0) or the original lieferando kitchen tags (1) ?")
while True:
    decision = input()
    # Use tag_correction to use custom categories of kitchen
    if decision == '0':
        helper = []
        for city in citys_scraped:
            helper.append(data_helper.tag_correction(city, kitchens))
        citys_scraped = helper
        break
    # Use Lieferdando categories
    elif decision == '1':
        break
    else:
        print("Invalid Input. Follow the instruction above!")

# Ask which type of plots
print("Enter 1, 2 or 3. \n")
if len(citys_scraped) > 2:
    print("Please select number. \n 1: Each city separately. \n 2: Plots with all cities represented. \n 3:  Separately and all cities represented.")
    while True:
        decision = input()
        if decision in ["1", "2", "3"]:
            decision = int(decision)
            break
        else:
            print("Invalid Input. Follow the instruction above!")

 
elif len(citys_scraped) == 2:
    print("Please select number. \n 1: Each city separately. \n 2: Plots with both cities represented.  \n 3: Separately and both cities represented.")
    while True:
        decision = input()
        if decision in ["1", "2", "3"]:
            decision = int(decision)
            break
        else:
            print("Invalid Input. Follow the instruction above!")

else:
    decision = 1

draw_options(decision, len(citys_scraped))

# Ask for the specific plots of interest
print("\nEnter the numbers of plots you are interested in or select 0 for all plots. Stop with 'x'.")

selection = []
while True:
    plot_type = input()
    if str.lower(plot_type) == "x":
        break
    elif str.lower(plot_type) == "0":
        selection = 0
        break
    elif str.lower(plot_type) in ['1', '2', '3', '4', '5', '6']:
        selection.append(int(plot_type))
    else:
        print("Invalid Input. Follow the instruction above!")

# Sort plots for pdf's
if selection == 0:
    selection = [1, 2, 3, 4, 5, 6]
# For all elements selected, add each plot for a selection to variables 
h_one = {city: [] for city in citys}
h_two = []
h_three  = []
for s in selection:
    selected_plots_one, selected_plots_two, selected_plots_three = get_plots(decision, len(citys_scraped), s, citys_scraped, citys)
    for city in citys:
        h_one[city] += selected_plots_one[city]
    h_two += selected_plots_two
    h_three += selected_plots_three
selected_plots_one = h_one
selected_plots_two = h_two
selected_plots_three = h_three

# create pdf for the plots
if decision == 1 or decision == 3:
    for city in citys:
        get_pdf(selected_plots_one[city], city + '.pdf')
if selected_plots_two:
    get_pdf(selected_plots_two, citys[0] + '_' + citys[1] + '.pdf')
if selected_plots_three:
    name = ''
    for city in citys:
        name += city
    get_pdf(selected_plots_three, name + '.pdf')
