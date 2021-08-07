# Functions for manipulating and flattening data

#TODO DOCSTRING REFINING
"""
helper function to get fitting key for value
params:
    d: the dictionary to be searched for a key
    val: the value to be searched for
return: fitting key or None if no key was found
"""
def get_keys_from_value(d: dict, val):

    key = [k for k, v in d.items() if val in v]

    if key:
        return key[0]
    else:
        return None

#TODO DOCSTRING REFINING
"""
Checks the given tags and changes them to class tags based on a dict of form {classtag: ["Subtag_1", "Subtag_2",...]}
params:
    restaurants: a list of restaurants in the form of scraper.py output
    tags: a dict of classtags as keys and subtags as values
return: list in same shape as input list
"""
def tag_correction(restaurants: list, tags: dict ) -> list:

    if restaurants:

        for kitchen in restaurants:
            
            i = 0

            while i < len(kitchen[1]):

                #change to class tag if possible
                new_tag = get_keys_from_value(tags, kitchen[1][i])

                if new_tag not in kitchen[1] and new_tag != None:

                    del kitchen[1][i]
                    kitchen[1].insert(0, new_tag)
                    i += 1

                else:

                    del kitchen[1][i]

            #if no classtag was found tag will be "Others"
            if not kitchen[1] or kitchen[1][0] == None:
                kitchen[1].append("Others")

    return restaurants
                    


def kitchen_counter(list_of_restaurants):
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
    count_kitchens, _ = kitchen_counter(list_of_restaurants)

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


"""
TODO DOCSTRING
"""
def get_all_kitchens(list_of_cities):

    all_kitchens = []

    for city in list_of_cities:
        prep, _ = kitchen_counter(city)
        all_kitchens.append(list(prep.keys()))

    all_kitchens = [item for sublist in all_kitchens for item in sublist]

    all_kitchens = list(dict.fromkeys(all_kitchens)) 

    return all_kitchens


"""
TODO DOCSTRING
"""
def kitchens_of_multiple_cities(list_of_cities, all_kitchens):
    number_kitchens = []


    for city in list_of_cities:
        helper = []
        prep, _ = kitchen_counter(city)
        for kitchen in all_kitchens:
            if kitchen not in prep.keys():
                helper.append(0)
            else: 
                helper.append(prep[kitchen])
        number_kitchens.append(helper)
    
    return number_kitchens



if __name__ == '__main__':
    pass