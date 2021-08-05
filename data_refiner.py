#File for refining and flatten the gathered data
import Levenshtein
import spacy
nlp = spacy.load('de_core_news_sm')
# input is a list of tuples
#(Restaurant (String), [Tag1, Tag2] (List of Strings), 
# #Lieferzeit# (int), Lieferkosten (double/float), Mindestbestellwert(double/float),
# Bewertung (double/float), Bewertungsanzahl (int))
# and must have tags and must_not have tags
def tag_correction(restaurants: list = [], w_tags: tuple = (), uw_tags: tuple = ()) -> list:
    tags = list()

    # check for tags
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
                
def similar_tags(tag_1, tag_2):
    
    doc1 = nlp(tag_1)
    doc2 = nlp(tag_2)

    for t in doc2:
        print(t.text, t.lemma_, t.pos_, t.tag_, t.dep_)

    for t1 in doc1:
        for t2 in doc2:
            if t1.lemma_ == t2.lemma_:
                return True

    return False
    '''
    sims = []
    s = "Test"
    tag_1 = tag_1.lower()
    tag_2 = tag_2.lower()
    t1 = tag_1.split()
    t2 = tag_2.split()
    for t in t1:
        for u in t2:
            sims.append((t, u, Levenshtein.ratio(t, u)))
    return sims'''



'''
Gedanken

Levenshtein gut schnell simpel, aber nicht zuverlässig
Stemming would be an option but how to differentiate between words like "gut" and "deutsch"
-> Lemmatisation would be slower but we could use Wordnet to delete "quality" and stop(filler) words
Language needs to be changed to en

'''


if __name__ == '__main__':
    s = similar_tags("italienische Küche", "gute Deutsche Küche")
    #s1 = similar_tags("afrikanisch", "asiatisch")
    print(s)
