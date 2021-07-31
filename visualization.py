import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np



def prepare_data(list_of_restaurants):

    #(Restaurant (String), [Tag1, Tag2] (List of Strings), 
    # #Lieferzeit# (int), Lieferkosten (double/float), Mindestbestellwert(double/float), 
    # Bewertung (double/float), Bewertungsanzahl (int)))

    list_of_kitchens = []

    for t in list_of_restaurants:
        list_of_kitchens += t[1]
    
    count_kitchens = {kitchen: list_of_kitchens.count(kitchen) for kitchen in list_of_kitchens}

    return count_kitchens, len(list_of_kitchens)

def sort_dict(unsorted_dict):
    sorted_dict = {}
    sorted_keys = sorted(unsorted_dict, key=unsorted_dict.get, reverse=True)

    for key in sorted_keys:
        sorted_dict[key] = unsorted_dict[key]

    return sorted_dict

def basic_pie(list_of_restaurants):

    count_kitchens, total_number_of_kitchens = prepare_data(list_of_restaurants)

    count_kitchens = sort_dict(count_kitchens)

    num_restaurants = len(list_of_restaurants)

    #TODO Think of better ways to come up with a good limit estimation 1 + 0.04 * num_restaurant 

    limit = 1 + 0.05 * num_restaurants
    '''
    if num_restaurants <= 25:
        limit = 1
    elif num_restaurants <= 50:
        limit = 3
    elif num_restaurants <= 100:
        limit = 5
    elif num_restaurants <= 300:
        limit = 10
    elif num_restaurants <= 500:
        limit = 20
    else:
        limit = 30'''

    kitchen_dict = {'others' : 0}
    other_kitchens = []
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
        sizes.append((kitchen/total_number_of_kitchens) * 100)
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

    #draw circle 
    centre = plt.Circle((0,0), 0.7, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre)

    #TODO legend for the kitchens with are included in others 

    ax1.axis('equal') #ensures that pie is drawn as a circle 
    plt.tight_layout()
    plt.show()


def basic_bar(list_of_restaurants):

    count_kitchens, total_number_of_kitchens = prepare_data(list_of_restaurants)

    count_kitchens = sort_dict(count_kitchens)

    labels = count_kitchens.keys()
    sizes = []
    colors = []
    cmap = ['darkred', 'red', 'orange', 'green', 'blue']

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

    width = 0.5

    fig, ax = plt.subplots()

    ax.bar(labels, sizes, width, color=colors)

    ax.set_ylabel('Procent')
    ax.set_title('Distributions of kitchens')

    patch1 = mpatches.Patch(color=cmap[0], label='1')
    patch2 = mpatches.Patch(color=cmap[1], label='<= 5')
    patch3 = mpatches.Patch(color=cmap[2], label='<= 25')
    patch4 = mpatches.Patch(color=cmap[3], label='<= 50')
    patch5 = mpatches.Patch(color=cmap[4], label='> 50')

    ax.legend(handles=[patch1, patch2, patch3, patch4, patch5])

    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.show()


def discrete_distribution(list_of_restaurants, kitchen_tags):

    category_names = ['very bad', 'bad', 'okay', 'good', 'very good']

    #TODO get all the restaurants with a certain kitchen and their reviews

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

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

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


            




    









   













    






        
        


