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
    if not w_tags is None:
        for i in range(len(restaurants)):

            for tag in restaurants[i][1]:
                if tag not in w_tags or tag in uw_tags:
                    restaurants[i][1].remove(tag)
            
            if not restaurants[i][1]:
                del restaurants[i]

                
                
            





if __name__ == '__main__':
    pass
