import cPickle
import re

def abbDictToPickle(dictionary):

    knownDiseases = []
    validatedAbbs = set()
    diseaseRegex = re.compile("([\w\-]*\s)*(cancer|disease|[\w\-]+(pathy|ia|osis|emia|itis|algia|megaly|oma|rrhea|rrhage|rrhagia|" \
                   "sclerosis|uria|ectomy|lysis|crine|dipsia|ism|lapse|mortem|ous|partum|phagia|phasia|plasm|plegia|pnea|" \
                   "stasis|tension|trophy|cele|ptysis))\s?$")



    # loads the data
    with open('databases/wikidata.pkl', 'rb') as f:
        knownDiseases = cPickle.load(f)

    validatedKeys = set()

    # regex only allows good abs and keys
    for key in dictionary:
        if key in knownDiseases or diseaseRegex.search(key):
            for abb in dictionary[key]:
                print key
                validatedAbbs.add(abb)
                validatedKeys.add(key)



    exisitingKnownAbbs = set()
    for value in validatedAbbs:
        exisitingKnownAbbs.add(value)

    with open('databases/diseaseAbbreviationsDatabase.pkl', 'wb') as f:
        cPickle.dump(exisitingKnownAbbs, f)

    with open('databases/wikiData.pkl', 'rb') as f:
        exisitingWikiDataKnowns = cPickle.load(f)

    for key in validatedKeys:
        if not key in exisitingWikiDataKnowns:
            exisitingWikiDataKnowns.append(key)

    with open('databases/wikiData.pkl', 'wb') as f:
        cPickle.dump(exisitingWikiDataKnowns, f)
