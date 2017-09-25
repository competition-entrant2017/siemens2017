import re

def getAcronymDictionary(text):
    acronymDictionary = dict()
    text = text
    matches = re.finditer("\([\w][\w\-]+\)", text)
    for match in matches:
        pattern = ""
        acronym = match.group()
        acronymChars = re.findall("[a-zA-Z\d]", acronym)
        followPattern = "([a-zA-Z]*\s|[a-zA-Z]*\-[a-zA-Z]*\s|\s?|[a-zA-Z]*\-|\-[a-zA-Z]*)"
        additonalWordFollowPattern = "([a-zA-Z]*\s|[a-zA-Z]*\-[a-zA-Z]*\s|\s?|[a-zA-Z]*\-|\-[a-zA-Z]*|[a-zA-Z]*\s[a-zA-Z]*\s)"
        endPattern = editAcronymToRegex(acronym)
        if len(acronymChars) == 2:
            pattern = "(" + str.lower(acronymChars[0]) + "|" + str.upper(acronymChars[0]) + ")" + "[a-zA-Z]*\s?" + \
                      "(" + str.lower(acronymChars[1]) + "|" + str.upper(acronymChars[1]) + ")" + "[a-zA-Z]*" + \
                      "\s?" + endPattern

        else:
            counter = 0
            for char in acronymChars:
                if counter == len(acronymChars) - 2:
                    pattern = pattern + "(" + str.lower(char) + "|" + str.upper(char) + ")" + additonalWordFollowPattern
                elif counter == len(acronymChars) - 1:
                    pattern = pattern + "(" + str.lower(char) + "|" + str.upper(
                        char) + ")" + additonalWordFollowPattern + endPattern
                else:
                    pattern = pattern + "(" + str.lower(char) + "|" + str.upper(char) + ")" + followPattern
                counter += 1
        acronym = re.search("[a-zA-Z\d\-]+", acronym).group()

        patterns = checkAcronymInAcronym(acronym, pattern, acronymDictionary)

        for patternObj in patterns:
            try:
                pattern = patternObj[0]
                acronym = patternObj[1]

                expandedAcronym = re.search(pattern=pattern, string=text).group()
                expandedAcronym = removeAcronyms(expandedAcronym)
                expandedAcronym = removeExtraWhiteSpace(expandedAcronym)
                expandedAcronym = replaceAcronyms(expandedAcronym, acronymDictionary)
                expandedAcronym = removeExtraWhiteSpace(expandedAcronym)

                if expandedAcronym in acronymDictionary:
                    acronymDictionary[expandedAcronym].add(acronym)
                else:
                    acronymDictionary[expandedAcronym] = set()
                    acronymDictionary[expandedAcronym].add(acronym)
            except:
                print ""

    return acronymDictionary




def editAcronymToRegex(acronym):
    indices = [m.start() for m in re.finditer('[\.\(\)\-]', acronym)]
    if len(indices) > 0:
        for index in reversed(indices):
            acronym = acronym[0:index] + "\\" + acronym[index:]
    return acronym


def removeAcronyms(text):
    acronymMatches = re.findall("\([a-zA-Z\d\-]*\)", text)
    for match in acronymMatches:
        index = text.find(match)
        if text[index - 1] is ' ':
            text = text.replace(" " + match, '')
        else:
            text = text.replace(match, '')
    return text


def replaceAcronyms(expandedAcronym, dictionaryAcronyms):
    for value in dictionaryAcronyms.items():
        for acronym in value[1]:
            if acronym in expandedAcronym:
                expandedAcronym = expandedAcronym.replace(acronym, value[0])

    return expandedAcronym


def checkAcronymInAcronym(acronym, pattern, dictionaryAcronyms):
    for entry in dictionaryAcronyms:
        key = entry
        for value in dictionaryAcronyms[key]:
            oldPattern = "(\-" + value + "\-|\-" + value + "|" + value + "\-)"
            matches = re.search(oldPattern, acronym)
            if matches is not None:
                # remove value from regex pattern and replace with key
                removeRegex = ""
                for char in re.findall("[a-zA-Z\d]", value):
                    literalFollowPatternOrAddtionalWord = "(\(\[a\-zA\-Z\]\*\\\s\|\[a\-zA\-Z\]\*\\\-\[a\-zA\-Z\]\*\\\s\|\\\s\?\|\[a\-zA\-Z\]\*\\\-\|\\\-\[a\-zA\-Z\]\*\)|\(\[a\-zA\-Z\]\*\\\s\|\[a\-zA\-Z\]\*\\\-\[a\-zA\-Z\]\*\\\s\|\\\s\?\|\[a\-zA\-Z\]\*\\\-\|\\\-\[a\-zA\-Z\]\*\|\[a\-zA\-Z\]\*\\\s\[a\-zA\-Z\]\*\\\s\))"
                    removeRegex = removeRegex + "\(" + str.lower(char) + "\|" + str.upper(
                        char) + "\)" + literalFollowPatternOrAddtionalWord

                removeString = re.search(pattern=removeRegex, string=pattern).group()
                # the pattern if there is another seperate acronym
                doubleAcronymPattern = pattern.replace(removeString, '')
                doubleAcronym = acronym.replace(matches.group(), '')
                newPattern = "(" + value + "(\s?|\-[a-zA-Z\d]*\s)" + "|" + key + "(\s\(" + value + "\)\-[a-zA-Z\d]*\s|\s?|\-[a-zA-Z\d]*\s))" + pattern.replace(
                    removeString, '')
                return [[newPattern, acronym], [doubleAcronymPattern, doubleAcronym]]
    # else case
    return [[pattern, acronym]]


def removeExtraWhiteSpace(text):
    length = len(text)
    if text[length - 1] is ' ':
        return text[:length - 1]
    else:
        return text



