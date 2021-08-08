import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import axes3d
from matplotlib import style
import numpy as np
from data_helper import kitchen_counter, sort_dict, get_average, get_all_kitchens, kitchens_averages_of_multiple_cities
import statistics
import math

#!!! Important, data manipulation and data helper moved to file "data_helper.py"
#!!! function  "prepare_data" renamed in "kitchen_counter"


def get_pdf(list_of_figures, pdf_name):
    '''Create a pdf with given plots in a list.
    
    list_of_figures : list of matplotlib figures
    pdf_name : str
        Name of the pdf file.
    '''
    #TODO make sure pdf_name is ending with .pdf

    pdf = PdfPages(pdf_name)

    for fig in list_of_figures:
        pdf.savefig(fig)
    
    pdf.close()

def basic_pie(list_of_restaurants, , city_name: str = ""):
    '''Return a pie plot which illustrates the distribution of kitchens.
    
    list_of_restaurants : [(Restaurant->str, [kitchen1->str, kitchen2->str,...], 
                        Lieferzeiten->int, Lieferkosten->float, Mindestbestellwert->float,
                        Bewertung->float, Bewertungsnazahl->int), ...]
    '''

    count_kitchens, total_number_of_kitchens = kitchen_counter(list_of_restaurants)
    count_kitchens = sort_dict(count_kitchens) 
    num_restaurants = len(list_of_restaurants)

    # limit to estimate the amount of kitchens included in the category 'others'
    limit = 1 + 0.05 * num_restaurants

    kitchen_dict = {'others' : 0} # Include the key 'others' 
    other_kitchens = []
    # Add keys and number of each kitchen to kitchen_dict
    for key in count_kitchens:
        if count_kitchens[key] > limit: 
            kitchen_dict[key] = count_kitchens[key]
        else: 
            kitchen_dict['others'] += count_kitchens[key]
            other_kitchens += key

    count_kitchens = sort_dict(kitchen_dict) 

    labels = count_kitchens.keys()
    sizes = []
    for kitchen in count_kitchens.values():
        sizes.append((kitchen/total_number_of_kitchens) * 100) # Calculate the procentages 
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.set_title("Distributions of kitchens " + city_name)

    #draw circle 
    centre = plt.Circle((0,0), 0.7, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre)

    #TODO legend for the kitchens with are included in others 

    ax1.axis('equal') #ensures that pie is drawn as a circle 
    plt.tight_layout()
    
    plt.show()
    return fig1

def bar(labels, sizes, colors, ylabel, title, patches=False):
    '''Return a bar plot.
    Keyword arguments:
    labels -- label of each bar
    sizes -- values of each bar
    colors -- color of each bar
    ylabel -- name of y-axis 
    title -- title for the plot
    patches -- include labels and colors for the legend (optional)
    '''

    fig, ax = plt.subplots()
    width = 0.5

    ax.bar(labels, sizes, width, color=colors)

    ax.set_ylabel(ylabel)
    ax.set_title(title)

    #Draw an average line
    if sizes != []:
        ax.axhline(statistics.mean(sizes), color='red', linewidth=2)

    if patches != False:
        ax.legend(handles=patches)

    plt.xticks(rotation=90)
    plt.tight_layout()

    return fig 

def avg_bar(list_of_restaurants, index, city_name: str = ""):
    '''Return a bar plot for averages.'''
    

    average = get_average(list_of_restaurants, index)

    labels = list(average.keys())
    sizes = list(average.values())
    
    # Set ylabel and title for each possible index 
    if index == 2:
        ylabel = "Average delivery time"
        title = "Comparison of the average delivery times per kitchen " + city_name
    elif index == 3:
        ylabel = "Average delivery cost"
        title = "Comparison of the average delivery cost per kitchen " + city_name
    elif index == 4:
        ylabel = "Average minimum amount for an order"
        title = "Comparison of the average minmum amounts for an order " + city_name
    elif index == 5:
        ylabel = "Average rating"
        title = "Comparison of the average rating for an order " + city_name
    
    # set the color
    colors = 'b'

    fig = bar(labels, sizes, colors, ylabel, title)

    plt.show()
    return fig

def basic_bar(list_of_restaurants, city_name: str = ""):
    '''Return a bar plot which illustrates the percentage of each kitchen with the total amount of each kitchen.'''

    count_kitchens, total_number_of_kitchens = kitchen_counter(list_of_restaurants)

    count_kitchens = sort_dict(count_kitchens)

    labels = count_kitchens.keys()
    sizes = []
    colors = []
    cmap = ['darkred', 'red', 'orange', 'green', 'blue']

    # Add the colors and the values in percent for the bars
    for kitchen in count_kitchens.values():
        sizes.append((kitchen/total_number_of_kitchens) * 100)
        if kitchen == 1:
            colors.append(cmap[0])
        elif kitchen <= 5:
            colors.append(cmap[1])
        elif kitchen <= 25:
            colors.append(cmap[2])
        elif kitchen <= 50:
            colors.append(cmap[3])
        else: 
            colors.append(cmap[4])

    # legend for illustrate the total amount of kitchens 
    patch1 = mpatches.Patch(color=cmap[0], label='1')
    patch2 = mpatches.Patch(color=cmap[1], label='<= 5')
    patch3 = mpatches.Patch(color=cmap[2], label='<= 25')
    patch4 = mpatches.Patch(color=cmap[3], label='<= 50')
    patch5 = mpatches.Patch(color=cmap[4], label='> 50')

    patches = [patch1, patch2, patch3, patch4, patch5]
    plot = bar(labels, sizes, colors, 'Percent', 'Distributions of kitchens ' + city_name, patches)
    
    plt.show()
    return plot

def discrete_distribution(list_of_restaurants, kitchen_tags, , city_name: str = ""):
    '''Return a horizontal bar plot which illustrates the ratings categorized in each kitchen.
    
    Keyword arguments:
    kitchen_tags -- list of kitchens to observe  
    '''

    category_names = ['very bad', 'bad', 'okay', 'good', 'very good']

    results = dict((kitchen, [0, 0, 0, 0, 0]) for kitchen in kitchen_tags)

    for restaurant in list_of_restaurants:
        restaurant_kitchen = set(restaurant[1])
        kitchen_tags = set(kitchen_tags)

        # Intersection of the restaurants kitchen and given kitchen in kitchen_tags
        incommon = kitchen_tags.intersection(restaurant_kitchen) 

        if len(incommon) > 0 and restaurant[6] > 0: # Check if there is an intersection and that the restaurant has reviews
            for kitchen in incommon:
                if restaurant[5] <= 1:
                    results[kitchen][0] += 1

                elif restaurant[5] <= 2:
                    results[kitchen][1] += 1

                elif restaurant[5] <= 3:
                    results[kitchen][2] += 1

                elif restaurant[5] <= 4:
                    results[kitchen][3] += 1

                elif restaurant[5] <= 5:
                    results[kitchen][4] += 1

    #TODO don't print 0 
    #TODO add comments
    
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                    label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
        

    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    ax.set_title("Rating distribution " + city_name)

    plt.show()
    return fig

def difference_plot(difference_dict, ylabel, title, values_city1, values_city2, patchlabel=False):
    ''' Compare the average differences of two cities.
    Keyword arguments: 
    difference_dict -- dictionary with kitchen as keys and the differences as values
    ylabel -- name of the yaxis
    title -- title of the plot
    values_city1, values_city2 -- values of both cities
    patchlabel -- include labels and colors for the legend (optional)
    '''
    
    colors = []
    cmap = ['blue', 'green', 'cornflowerblue', 'mediumspringgreen']
    # Add a color for each bar
    for difference in difference_dict:
        if values_city2[difference] == 0:
            colors.append(cmap[2])
        elif values_city1[difference] == 0:
            colors.append(cmap[3])
        elif difference_dict[difference] >= 0:
            colors.append(cmap[0])
        else:
            colors.append(cmap[1])

    labels = difference_dict.keys()
    sizes = list(difference_dict.values())

    if patchlabel != False:
        if len(patchlabel) == 2:
            patch1 = mpatches.Patch(color=cmap[0], label=patchlabel[0])
            patch2 = mpatches.Patch(color=cmap[1], label=patchlabel[1])
            patchlabel = [patch1, patch2]
        elif len(patchlabel) == 4:
            patch1 = mpatches.Patch(color=cmap[0], label=patchlabel[0])
            patch2 = mpatches.Patch(color=cmap[1], label=patchlabel[1])
            patch3 = mpatches.Patch(color=cmap[2], label=patchlabel[2])
            patch4 = mpatches.Patch(color=cmap[3], label=patchlabel[3])
            patchlabel = [patch1, patch2, patch3, patch4]


    fig = bar(labels, sizes, colors, ylabel, title, patchlabel)
    plt.axhline(y=0, color='black', linestyle='-')

    return fig

def kitchen_difference(city1, city2, adress1, adress2):
    '''Bar plot to compare the differences of the amount of each kitchen in two cities.
    
    Keyword arguments: 
    city1, city2 -- list of restaurants for each city
    adress1, adress2 -- name of the adress of each city'''

    count_kitchens_c1, _ = kitchen_counter(city1)
    count_kitchens_c2, _ = kitchen_counter(city2)

    all_kitchen = list(dict.fromkeys(list(count_kitchens_c1.keys()) + list(count_kitchens_c2.keys())))

    differ = dict((i, 0) for i in all_kitchen) 
    
    # Calculate the differences 
    for kitchen in differ:
        if kitchen not in count_kitchens_c1:
            count_kitchens_c1[kitchen] = 0
        if kitchen not in count_kitchens_c2:
            count_kitchens_c2[kitchen] = 0
        differ[kitchen] = count_kitchens_c1[kitchen] - count_kitchens_c2[kitchen]
    differ = sort_dict(differ)

    ylabel = "difference of the amount of kitchens"
    title = 'Distributions of kitchens in ' + adress1 + " and " + adress2
    patchlabels = [adress1, adress2, "only " + adress1, "only " + adress2]

    fig = difference_plot(differ, ylabel, title, count_kitchens_c1, count_kitchens_c2, patchlabels)
    plt.show()
    return fig
    
def average_difference(city1, city2, adress1, adress2, index):

    average_city1 = get_average(city1, index)
    average_city2 = get_average(city2, index)

    #count_kitchens_c1 , _ = kitchen_counter(city1)
    #count_kitchens_c2 , _ = kitchen_counter(city2)

    kitchen_intersection = set(average_city1.keys()).intersection(set(average_city2.keys()))

    rating_difference_dict = dict((kitchen, 0) for kitchen in kitchen_intersection)

    for kitchen in rating_difference_dict:
        rating_difference_dict[kitchen] = average_city1[kitchen] - average_city2[kitchen]

    patchlabels = False
    if index == 2:
        ylabel = "difference of the average delivery time of each kitchen"
        title = "Delivery time Differences in" + adress1 + " and " + adress2
        patchlabels = [adress1, adress2]
    elif index == 3:
        ylabel = "difference of the average delivery cost of each kitchen"
        title = "Delivery Cost Differences in " + adress1 + " and " + adress2
        patchlabels = [adress1, adress2, adress2 + ': Free', adress1 + ': Free']
    elif index == 4:
        ylabel = "difference of the average mimium order cost of each kitchen"
        title = "Minimum Order Cost Differences in " + adress1 + " and " + adress2
        patchlabels = [adress1, adress2]
    elif index ==5:
        ylabel = "difference of the average ratings of each kitchen"
        title = "Rating Differences in " + adress1 + " and " + adress2
        patchlabels = [adress1, adress2, adress2 + ' has no review', adress1 + ' has no review']

    fig = difference_plot(rating_difference_dict, ylabel, title, average_city1, average_city2, patchlabels)
    plt.show()
    return fig
    
def multiple_bars_num_of_kitchens(list_of_cities, list_of_city_names, list_kitchen=[]):
    '''3D plot with multiple bars, to illustrate the amount of kitchens per city.
    
    Keyword arguments: 
    list_of_cities -- list of lists with restaurants for each city
    list_of_city_names -- name of all cities 
    list_kitchen -- kitchen to observe (optional)'''

    number_cities = len(list_of_city_names) # number of cities we want to compare

    all_kitchens = []

    if list_kitchen != []:
        all_kitchens = list_kitchen # Use the kitchens provided by the optional input list_kitchen
        
    else:
        all_kitchens = get_all_kitchens(list_of_cities)
        
    number_kitchens, _ = kitchens_averages_of_multiple_cities(list_of_cities, all_kitchens)
        
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    colors = []
    cmap = ['r', 'g', 'b', 'y'] 
    yticks = []

    for i in range(number_cities):
        colors.append(cmap[i%len(cmap)]) #if more than 4 cities, then reuse the colors
        yticks.append(number_cities-i)
    

    for a, b, i in zip(colors, yticks, range(number_cities)):

        xs = np.arange(len(all_kitchens))
        #xs = [5*i for i in xs] #TODO check if necessary 
        ys = number_kitchens[i]

        plt.xticks(xs, all_kitchens, rotation=90)
        
        cs = [a] * len(xs)

        ax.bar(xs, ys, zs=b, zdir='y', color=cs, alpha=0.8)

    plt.yticks(yticks, list_of_city_names, rotation=90)
    ax.set_zlabel('Total number of kitchens')
    #plt.tick_params(axis='x', which='major', labelsize=7)

    plt.tight_layout()

    plt.show()

    return fig

def heatmap(list_of_cities, list_of_city_names, index=-1): #TODO check if amount of kitchens correct
    '''Compare cities amount of kitchen or averages in a heatmap.'''

    number_cities = len(list_of_city_names) # number of cities we want to compare

    all_kitchens = get_all_kitchens(list_of_cities)
        
    num_of_kitchens, num_of_averages = np.array(kitchens_averages_of_multiple_cities(list_of_cities, all_kitchens, index), dtype=object)

    title = "Num of kitchen in each city"
    data = num_of_kitchens

    if num_of_averages != []:
        data = num_of_averages # If index is given, then use averages
        if index == 2:
            title = "Average of delivery time in each city per kitchen"
        elif index == 3:
            title = "Average of delivery cost in each city per kitchen"
        elif index == 4:
            title = "Average of the minium order amount in each city per kitchen"
        elif index == 5:
            title = "Average of the ratings in each city per kitchen"

    fig, ax = plt.subplots()

    if -1 in data:
        im = ax.imshow(data, cmap='inferno')
        
        maximum = max(max(data)) #Get the maximum 
        
        ticks = np.linspace(0, maximum, 8) 
        ticks = np.insert(ticks, 0, -1, axis=0)
        ticks = ticks[ticks != 0] # Delete zero, else it would be to close to -1

        cbar = fig.colorbar(im, ticks=ticks)
        labels = []
        for tick in ticks:
            if tick == -1:
                labels.append('Closed for delivery')
            else:
                labels.append(str(math.floor(tick))) #TODO evtl. besser Runden auf 5er bzw. 10er
        cbar.ax.set_yticklabels(labels)        
    else: 
        im = ax.imshow(data, cmap='inferno')
        fig.colorbar(im)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(all_kitchens)))
    ax.set_yticks(np.arange(len(list_of_city_names)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(all_kitchens)
    ax.set_yticklabels(list_of_city_names)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    ax.set_title(title)
    fig.tight_layout()
    plt.show()

    return fig