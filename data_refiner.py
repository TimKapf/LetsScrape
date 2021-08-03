#File for refining and flatten the gathered data

# input is a list of tuples
#(Restaurant (String), [Tag1, Tag2] (List of Strings), 
# #Lieferzeit# (int), Lieferkosten (double/float), Mindestbestellwert(double/float),
# Bewertung (double/float), Bewertungsanzahl (int))
# and must have tags and must_not have tags
def tag_correction(restaurants: list = [], w_tags: tuple = (), uw_tags: tuple = ()) -> list:
    tags = list()

    # check for tags and delete empty entrys
    # TODO need to be tested
    '''
    if not ((not w_tags and not uw_tags) or not restaurants):
        for i in range((len(restaurants)-2)):

            for tag in restaurants[i][1]:
                if tag not in w_tags or tag in uw_tags:
                    restaurants[i][1].remove(tag)
            
            if not restaurants[i][1]:
                del restaurants[i]

    return restaurants
'''
    if not ((not w_tags and not uw_tags) or not restaurants):
        i = 0
        while i < len(restaurants)-1:
            j = 0
            while j < len(restaurants[i][1]):
                if (restaurants[i][1][j] not in w_tags and w_tags) or restaurants[i][1][j] in uw_tags:
                    del restaurants[i][1][j]
                    j -= 1
                j+=1
            
            if not restaurants[i][1]:
                del restaurants[i]
                i -= 1
            i+=1

    return restaurants
                
            





if __name__ == '__main__':
    pass
