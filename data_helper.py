from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
# Functions for manipulating and flattening data


def get_keys_from_value(d: dict, val: object) -> object:

    """Find fitting key for value 'val' in dictionary d and return it."""
    key = [k for k, v in d.items() if val in v]

    if key:
        return key[0]
    else:
        return None


def tag_correction(restaurants: list, tags: dict ) -> list:

    """Change the tags of the restaurants to their upperclass equivalents or if not possible to 'Others'.

    Keyword arguments:
    restaurants -- [(restaurant_name: str, [type_kitchen1: str, type_kitchen2: str,...]: list, 
                        time_of_delivery: int, delivery_costs: float, min_order_value: float,
                        rating: float, number_of_ratings: int): tuple, ...]: list
    tags        -- A dictionary with upperclass tags as keys and a tuple with subtags as values
    """
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
                    


def kitchen_counter(restaurants: list) -> tuple:
    """ 1. Return a dictionary with kitchens as keys and the number of kitchens as value. 
        2. Return the total amount of kitchens.
    
    restaurants -- see description at tag_correction(restaurants, tags)
    """ 
    list_of_kitchens = []

    # Collect all kitchens
    for t in restaurants:
        list_of_kitchens += t[1]
    
    # Create dictionary 
    count_kitchens = {kitchen: list_of_kitchens.count(kitchen) for kitchen in list_of_kitchens}

    return (count_kitchens, len(list_of_kitchens))


#TODO Name anpassen e.g. sort_dict_descending()
def sort_dict(unsorted: dict) -> dict:

    """Returns a dictionary in descending order."""
    sorted_dict = {}
    # Sort the keys in descending order
    sorted_keys = sorted(unsorted, key=unsorted.get, reverse=True)

    # Add data to the keys
    for key in sorted_keys:
        sorted_dict[key] = unsorted[key]

    return sorted_dict


def get_average(restaurants: list, index: int): 
    """Calculate the average.
    
    Keyword arguments:
    restaurants -- see tag_correction(restaurants, tags)
    #TODO Was passiert bei 1?
    index       --  2: Average of delivery time 
                    3: Average of delivery cost
                    4: Average of minimum order amount
                    5: Average of the ratings
    """
    #TODO probablity more efficient version or better to just use mean()
    
    if index in [2, 3, 4, 5]: 

        list_of_kitchens = []

        # Collect all kitchens 
        for restaurant in restaurants:
            if restaurant[index] != -1: # If -1: Then there is no information about the value currently (e.g. restaurant is closed) 
                list_of_kitchens += restaurant[1]
        
        # Create dictionary with a list of two elements: 0: Add all values 1: Total number of added values
        average = {kitchen: [0,0] for kitchen in list_of_kitchens}

        for restaurant in restaurants:
            for kitchen in restaurant[1]:
                if restaurant[index] != -1:
                    # Restaurants with zero reviews will not be included
                    if not(index == 5 and restaurant[6] == 0):  

                        average[kitchen][0] += restaurant[index]
                        average[kitchen][1] += 1

        average = {kitchen: (average[kitchen][0] / average[kitchen][1]) for kitchen in list(average.keys())}

        return average



def get_all_kitchens(cities: list) -> list:
    """Return all kitchens of multiple cities.
    
    Keyword arguments:
    cities -- List with lists of restaurants as elements
    """

    all_kitchens = []

     # add all kitchens
    for city in cities:

        prep, _ = kitchen_counter(city)
        all_kitchens.append(list(prep.keys()))

    # no sublists
    all_kitchens = [item for sublist in all_kitchens for item in sublist]

    # delete duplicates
    all_kitchens = list(dict.fromkeys(all_kitchens)) 

    return all_kitchens


def kitchens_averages_of_multiple_cities(cities: list, all_kitchens: list, index: int =-1) -> tuple:
    """Return the number of cities and the average of a given index as a list of lists with values.
    Keyword arguments:
    cities       -- List with list of restaurants as elements
    all_kitchens -- List of kitchens
    index        --    -1: no average (default)
                        2: Averages of delivery time 
                        3: Averages of delivery cost
                        4: Averages of minimum order amount
                        5: Averages of the ratings
    """
    number_kitchens = []
    average = []
    
    # Create a list for all cities and append the numbers/averages for all kitchens.  
    for city in cities:

        helper1 = []
        helper2 = []
        prep, _ = kitchen_counter(city)

        if index != -1:
            avg = get_average(city, index)
        else:
            avg = get_average(city, 2) 

        for kitchen in all_kitchens:

            if kitchen not in prep.keys():

                helper1.append(0)
                helper2.append(-1)

            elif kitchen not in avg.keys():

                helper2.append(-1)
                helper1.append(prep[kitchen])

            else: 

                helper1.append(prep[kitchen])
                helper2.append(avg[kitchen])
                
        #Append the lists for each cities
        number_kitchens.append(helper1) 
        average.append(helper2)

    if index == -1: 
        average = []
    
    return number_kitchens, average

def get_number(String: str) -> float: #TODO  variable klein schrieben 
	"""This function returns the numbers of type float which appear in the given String. Lieferando.de uses the german format to represent point numbers, therefore "," will be transformed to ".".
	 Only works for the german format."""
    #TODO Error potential if more than one , 
	result = ''.join(x for x in String if x.isdigit() or x == ',')
	if result == "":
		return -1.0
	result = float(result.replace(',','.'))
	return result

def explicit_wait(driver: webdriver.Chrome, class_name: str, waiting_time: int):
    
    try:
	    my_elem = WebDriverWait(driver, waiting_time).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
	except TimeoutException:
		pass



if __name__ == '__main__':
    pass
