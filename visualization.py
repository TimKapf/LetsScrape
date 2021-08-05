import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import axes3d
from matplotlib import style
import numpy as np

def prepare_data(list_of_restaurants):
    '''1. Return a dictionary with kitchens as keys and the number of kitchens as value. 2. Return the total amount of kitchens.
    
    list_of_restaurants : [(Restaurant->str, [kitchen1->str, kitchen2->str,...], 
                        Lieferzeiten->int, Lieferkosten->float, Mindestbestellwert->float,
                        Bewertung->float, Bewertungsnazahl->int), ...]
    ''' 
    list_of_kitchens = []

    # Collect all kitchens
    for t in list_of_restaurants:
        list_of_kitchens += t[1]
    
    # Create dictionary 
    count_kitchens = {kitchen: list_of_kitchens.count(kitchen) for kitchen in list_of_kitchens}

    return count_kitchens, len(list_of_kitchens)

def sort_dict(unsorted_dict):
    '''Returns a dictionary in descending order.
    
    unsorted_dict : dict
    '''

    sorted_dict = {}
    # Sort the keys in descending order
    sorted_keys = sorted(unsorted_dict, key=unsorted_dict.get, reverse=True)

    # Add data to the keys
    for key in sorted_keys:
        sorted_dict[key] = unsorted_dict[key]

    return sorted_dict

def average_rating(list_of_restaurants):
    '''Return the average rating of each kitchen in a dictionary with the kitchens as keys 
    and the ratings as values
    
    list_of_restaurants : [(Restaurant->str, [kitchen1->str, kitchen2->str,...], 
                        Lieferzeiten->int, Lieferkosten->float, Mindestbestellwert->float,
                        Bewertung->float, Bewertungsnazahl->int), ...]
    '''
    count_kitchens, _ = prepare_data(list_of_restaurants)

    average = dict((kitchen, 0) for kitchen in list(count_kitchens.keys()))

    # Collect the ratings and add the rating to each kitchen in the dictionary
    for restaurant in list_of_restaurants: 
        review = restaurant[5]
        restaurant_kitchen = set(restaurant[1])
        for kitchen in restaurant_kitchen:
            average[kitchen] += review 

    # Calculate the average 
    for key in average:
        average[key] /= count_kitchens[key]

    return average

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

def basic_pie(list_of_restaurants):
    '''Return a pie plot which illustrates the distribution of kitchens.
    
    list_of_restaurants : [(Restaurant->str, [kitchen1->str, kitchen2->str,...], 
                        Lieferzeiten->int, Lieferkosten->float, Mindestbestellwert->float,
                        Bewertung->float, Bewertungsnazahl->int), ...]

    '''

    count_kitchens, total_number_of_kitchens = prepare_data(list_of_restaurants)
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
    ax1.set_title("Distributions of kitchens")

    #draw circle 
    centre = plt.Circle((0,0), 0.7, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre)

    #TODO legend for the kitchens with are included in others 

    ax1.axis('equal') #ensures that pie is drawn as a circle 
    plt.tight_layout()
    
    return fig1


def basic_bar(list_of_restaurants):
    '''Return a bar plot which illustrates the percentage of each kitchen 
    and the total amount of each kitchen.'''

    count_kitchens, total_number_of_kitchens = prepare_data(list_of_restaurants)

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

    fig, ax = plt.subplots()
    width = 0.5

    ax.bar(labels, sizes, width, color=colors)

    ax.set_ylabel('Percent')
    ax.set_title('Distributions of kitchens')

    # legend for illustrate the total amount of kitchens 
    patch1 = mpatches.Patch(color=cmap[0], label='1')
    patch2 = mpatches.Patch(color=cmap[1], label='<= 5')
    patch3 = mpatches.Patch(color=cmap[2], label='<= 25')
    patch4 = mpatches.Patch(color=cmap[3], label='<= 50')
    patch5 = mpatches.Patch(color=cmap[4], label='> 50')

    ax.legend(handles=[patch1, patch2, patch3, patch4, patch5])

    plt.xticks(rotation=90)
    plt.tight_layout()

    return fig


def discrete_distribution(list_of_restaurants, kitchen_tags):
    '''Return a horizontal bar plot which illustrates the ratings categorized in each kitchen.'''

    category_names = ['very bad', 'bad', 'okay', 'good', 'very good']

    results = dict((kitchen, [0, 0, 0, 0, 0]) for kitchen in kitchen_tags)

    for restaurant in list_of_restaurants:
        restaurant_kitchen = set(restaurant[1])
        kitchen_tags = set(kitchen_tags)

        incommon = kitchen_tags.intersection(restaurant_kitchen)

        if len(incommon) > 0 and restaurant[6] > 0:
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

    plt.show()

def kitchen_difference(city1, city2, adress1, adress2):

    count_kitchens_c1, _ = prepare_data(city1)
    count_kitchens_c2, _ = prepare_data(city2)

    #TODO Create dict with differences

    all_kitchen = list(dict.fromkeys(list(count_kitchens_c1.keys()) + list(count_kitchens_c2.keys())))

    differ = dict((i, 0) for i in all_kitchen)
    colors = []
    cmap = ['blue', 'green', 'cornflowerblue', 'mediumspringgreen']


    #TODO VARIABLENNAME falsch
    for kit in differ:
        if kit not in count_kitchens_c1:
            count_kitchens_c1[kit] = 0
        if kit not in count_kitchens_c2:
            count_kitchens_c2[kit] = 0
        differ[kit] = count_kitchens_c1[kit] - count_kitchens_c2[kit]
    differ = sort_dict(differ)

    for v in differ:    
        if differ[v] >= 0:
            if count_kitchens_c2[v] == 0:
                colors.append(cmap[2])
            else:
                colors.append(cmap[0])
        else:
            if count_kitchens_c1[v] == 0:
                colors.append(cmap[3])
            else:
                colors.append(cmap[1])
    

    fig, ax = plt.subplots()

    labels = differ.keys()
    width = .85
    sizes = list(differ.values())

    ax.bar(labels, sizes, width, color=colors)
    ax.set_ylabel("difference of the amount of kitchens")
    ax.set_title('Distributions of kitchens')
    plt.axhline(y=0, color='black', linestyle='-')

    patch1 = mpatches.Patch(color=cmap[0], label= adress1)
    patch2 = mpatches.Patch(color=cmap[2], label= "only " + adress1)
    patch3 = mpatches.Patch(color=cmap[1], label= adress2)
    patch4 = mpatches.Patch(color=cmap[3], label= "only " + adress2)
    ax.legend(handles=[patch1, patch2, patch3, patch4])

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return fig

def rating_difference(city1, city2, adress1, adress2):

    average_city1 = average_rating(city1)
    average_city2 = average_rating(city2)

    count_kitchens_c1 , _ = prepare_data(city1)
    count_kitchens_c2 , _ = prepare_data(city2)

    kitchen_intersection = set(count_kitchens_c1.keys()).intersection(set(count_kitchens_c2.keys()))

    rating_difference_dict = dict((kitchen, 0) for kitchen in kitchen_intersection)

    colors = []
    cmap = ['blue', 'green', 'cornflowerblue', 'mediumspringgreen']

    for kitchen in rating_difference_dict:
        rating_difference_dict[kitchen] = average_city1[kitchen] - average_city2[kitchen]
        if average_city2[kitchen] == 0:
            colors.append(cmap[2])
        elif average_city1[kitchen] == 0:
            colors.append(cmap[3])
        elif rating_difference_dict[kitchen] >= 0:
            colors.append(cmap[0])
        else:
            colors.append(cmap[1])
    
    fig, ax = plt.subplots()

    labels = rating_difference_dict.keys()
    width = .85
    sizes = list(rating_difference_dict.values())

    ax.bar(labels, sizes, width, color=colors)
    ax.set_ylabel("rating difference of the average ratings of each kitchen")
    #ax.set_title('')
    plt.axhline(y=0, color='black', linestyle='-')

    patch1 = mpatches.Patch(color=cmap[0], label= adress1)
    patch2 = mpatches.Patch(color=cmap[1], label= adress2)
    patch3 = mpatches.Patch(color=cmap[2], label= adress2 + ' has no review')
    patch4 = mpatches.Patch(color=cmap[3], label= adress1 + ' has no review')
    ax.legend(handles=[patch1, patch3, patch2, patch4])

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return fig

def multiple_bars_num_of_kitchens(list_of_cities, list_of_city_names, list_kitchen=[]):

    number_cities = len(list_of_city_names) # number of cities we want to compare

    all_kitchens = []

    if list_kitchen != []:
        all_kitchens = list_kitchen # Use the kitchens provided by the optional input list_kitchen
        
    else:
        for city in list_of_cities:
            prep, _ = prepare_data(city)
            all_kitchens.append(list(prep.keys()))

        all_kitchens = [item for sublist in all_kitchens for item in sublist]

        all_kitchens = list(dict.fromkeys(all_kitchens)) 
        

    number_kitchens = []

    for city in list_of_cities:
        helper = []
        prep, _ = prepare_data(city)
        for kitchen in all_kitchens:
            if kitchen not in prep.keys():
                helper.append(0)
            else: 
                helper.append(prep[kitchen])
        number_kitchens.append(helper)
        
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    colors = []
    cmap = ['r', 'g', 'b', 'y']
    yticks = []

    for i in range(number_cities):
        colors.append(cmap[i%len(cmap)])
        yticks.append(number_cities-i)

    y_pos = []

    for a, b, i in zip(colors, yticks, range(number_cities)):

        xs = np.arange(len(all_kitchens))
        xs = [5*i for i in xs]
        ys = number_kitchens[i]

        plt.xticks(xs, all_kitchens, rotation=90)
        
        cs = [a] * len(xs)

        y_pos.append(b)

        ax.bar(xs, ys, zs=b, zdir='y', color=cs, alpha=0.8, width=2)


    plt.yticks(y_pos, list_of_city_names)
    
    ax.set_zlabel('Total number of kitchens')

    plt.tick_params(axis='x', which='major', labelsize=7)

    plt.tight_layout()

    plt.show()

#TODO e.g. headmap and def above have same calc. for the listoflist of numbers 

def headmap(list_of_cities, list_of_city_names):

    number_cities = len(list_of_city_names) # number of cities we want to compare

    all_kitchens = []

    for city in list_of_cities:
        prep, _ = prepare_data(city)
        all_kitchens.append(list(prep.keys()))

    all_kitchens = [item for sublist in all_kitchens for item in sublist]

    all_kitchens = list(dict.fromkeys(all_kitchens)) 
        
    number_kitchens = []

    for city in list_of_cities:
        helper = []
        prep, _ = prepare_data(city)
        for kitchen in all_kitchens:
            if kitchen not in prep.keys():
                helper.append(0)
            else: 
                helper.append(prep[kitchen])
        number_kitchens.append(helper)

    city_names = list_of_city_names
    kitchen_names = all_kitchens 

    num_of_kitchens = np.array(number_kitchens)

    fig, ax = plt.subplots()
    im = ax.imshow(num_of_kitchens, cmap='inferno')
    fig.colorbar(im)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(kitchen_names)))
    ax.set_yticks(np.arange(len(city_names)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(kitchen_names)
    ax.set_yticklabels(city_names)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
            rotation_mode="anchor")

    ax.set_title("Num of kitchen in each city")
    fig.tight_layout()
    plt.show()






#def multiple_bars_average_ratings()
        