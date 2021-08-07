#File for refining and flatten the gathered data

# 
#(Restaurant (String), [Tag1, Tag2] (List of Strings), 
# #Lieferzeit# (int), Lieferkosten (double/float), Mindestbestellwert(double/float),
# Bewertung (double/float), Bewertungsanzahl (int))
# and a dictionary in form {classtag: (subtag1, subtag2) }
#TODO auf Dictionary anpassen

def get_keys_from_value(d, val):
    key = [k for k, v in d.items() if val in v]
    if key:
        return key[0]
    else:
        return None


#TODO needs testing
def tag_correction(restaurants: list, tags: dict ) -> list:


    if restaurants:
        for kitchen in restaurants:
            
            i = 0
            while i < len(kitchen[1]):
                new_tag = get_keys_from_value(tags, kitchen[1][i])
                if new_tag not in kitchen[1] and new_tag != None:
                    del kitchen[1][i]
                    kitchen[1].insert(0, new_tag)
                    i += 1
                else:
                    del kitchen[1][i]
            
            if not kitchen[1] or kitchen[1][0] == None:
                kitchen[1].append("Others")

    return restaurants
                    


    # check for tags
    '''if not ((not w_tags and not uw_tags) or not restaurants):
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

    return restaurants'''
                




if __name__ == '__main__':
    a = get_keys_from_value({"Italienisch": ["Italienische Pizza", "Pasta"],
            "Asiatisch": ["Japanisch", "Sushi", "Chinesisch"]}, "Italienische Pizza")
    print(a[0])