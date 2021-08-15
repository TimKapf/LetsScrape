import visualization
from matplotlib.backends.backend_pdf import PdfPages

def get_pdf(list_of_figures: list, pdf_name: str) -> None:
    """Create a pdf with given plots in a list.
    
    Keyword arguments:
    list_of_figures -- list of matplotlib figures
    pdf_name        -- Name of the pdf file.
    """
    # save pdf in a file called 'Output' which is located in the project file LetsScrape
    pdf = PdfPages('Output/' + pdf_name)

    # Add plot to pdf file
    for fig in list_of_figures:
        pdf.savefig(fig)
    
    pdf.close()

def draw_options(mode: int, number_cities: int, start_range: int=1):
    """Print out possiple actions in the terminal.
    
    Keyword arguments:
    mode            -- mode the user choose ealier 
    number_cities   -- number of cities to compare
    start_range     -- to enumerate correctly for mode 3
    """
    # Options to choose from 
    plots_one = ['Pie plot (Amount of kitchens)', 'Bar plot (Amount of kitchens)', 'Bar plot (Averages)']
    plots_two = ['Bar plot (Amount of kitchens)', 'Bar plot (Averages)']
    plots_multiple = ['3D bar plots (Amount of kitchens)', 'Heatmap (Amount of kitchens)', 'Heatmap (Averages)']

    # Print Options in the terminal 
    if mode == 1:
        print("Separate plots: \n")
        for plot, i in zip(plots_one, range(1, len(plots_one) + 1)):
            print(str(i) + ": " + plot)
    elif mode == 2:
        if number_cities == 2:
            print("Two city plots: \n")
            for plot, i in zip(plots_two, range(start_range, len(plots_two) + start_range)):
                print(str(i) + ": " + plot)
        elif number_cities > 2:
            print("Multiple city plots: \n")
            for plot, i in zip(plots_multiple, range(start_range, len(plots_multiple) + start_range)):
                print(str(i) + ": " + plot)
    elif mode == 3: 
        draw_options(1, number_cities)
        draw_options(2, number_cities, len(plots_one) + 1)

def avg_options() -> list:
    """Print out and select the averages the user can choose of."""

    print("Enter \n\n0: All\n1: Average delivery time per kitchen\n2: Average delivery cost per kitchen\n3: Average minimum order cost per kitchen\n4: Average rating per kitchen\n")
    selections = []
    # get (only relevant) selections
    while True:
        avg = input()
        if str.lower(avg) == 'x':
            break
        elif str.lower(avg) == '0':
            selections = [1, 2, 3, 4]
            break
        elif str.lower(avg) in ['1', '2', '3', '4']:
            selections.append(int(avg))

    return selections
        
def get_plots(mode: int, number_cities: int, selection: int, scraped_cities: list, name_cities: list, start_selection: int=1) -> tuple:
    """Add the plots the user is interested in to a list.
    
    Keyword arguments:
    mode                -- mode the user choose ealier 
    number_cities       -- number of cities to compare
    selection           -- number the user selected
    scraped_cities      -- formatted string by scraper.py
    name_cities         -- name of the scraped cities
    start_selection     -- to enumerate correctly for mode 3
    """
    # plots for each city are in different pdf file, therefore we use a dictionary with the cities as keys
    selected_plots_one = {city: [] for city in name_cities}
    # plots where at least two cities get compared only require one file, therefore a list is sufficient 
    selected_plots_two = []
    selected_plots_three = []

    # get all plots which the user selected

    # Plots for one city
    if mode == 1:
        if selection == 1:
            for s_city, n_city in zip(scraped_cities, name_cities):
                selected_plots_one[n_city].append(visualization.basic_pie(s_city, n_city))
        if selection == 2:
            for s_city, n_city in zip(scraped_cities, name_cities):
                selected_plots_one[n_city].append(visualization.basic_bar(s_city, n_city))
        if selection == 3:
            selection_avg = avg_options()
            for s_city, n_city in zip(scraped_cities, name_cities):
                for avg_type in selection_avg:
                    avg_type += 1
                    selected_plots_one[n_city].append(visualization.avg_bar(s_city, avg_type, n_city)) 
    # Plots for multiple cities
    elif mode == 2:
        if number_cities == 2:
            if selection == start_selection: 
                selected_plots_two.append(visualization.kitchen_difference(scraped_cities[0], scraped_cities[1], name_cities[0], name_cities[1]))
            elif selection == start_selection + 1:
                selection_avg = avg_options()
                for avg_type in selection_avg:
                    avg_type += 1
                    selected_plots_two.append(visualization.avg_difference(scraped_cities[0], scraped_cities[1], name_cities[0], name_cities[1], avg_type))
        if number_cities > 2:
            if selection == start_selection:
                selected_plots_three.append(visualization.kitchen_distribution_3D(scraped_cities, name_cities))
            elif selection == start_selection + 1:
                selected_plots_three.append(visualization.heatmap(scraped_cities, name_cities))
            elif selection == start_selection + 2:
                selection_avg = avg_options()
                for avg_type in selection_avg:
                    avg_type += 1
                    selected_plots_three.append(visualization.heatmap(scraped_cities, name_cities, avg_type))
    # Mode 3 is Mode 1 and Mode 2 combined (Recursion)
    elif mode == 3:
        if selection < 4:
            return get_plots(1, number_cities, selection, scraped_cities, name_cities) 
        else:
            return get_plots(2, number_cities, selection, scraped_cities, name_cities, 4) 

    return selected_plots_one, selected_plots_two, selected_plots_three