from acronymExpansion import *
import xml.etree.ElementTree as ET
import unidecode

def getAcronymDictionaryFromPubMedXML(XMLfilename):
    tree = ET.parse(XMLfilename)
    e = tree.getroot()

    acronymDictionary = dict()
    for set in e.iter('PubmedArticleSet'):
        for article in set.iter('PubmedArticle'):
            for next in article.iter('MedlineCitation'):
                for abstract in next.iter('Abstract'):
                    for abstractText in abstract.iter('AbstractText'):
                        text = abstractText.text
                        if text is not None:
                            if not type(text) == type(unicode()):
                                text = unicode(text, encoding='utf-8')
                            fixedText = unidecode.unidecode(text)
                            abstractAcronymDictionary = getAcronymDictionary(fixedText)
                            acronymDictionary = mergeDicts(acronymDictionary, abstractAcronymDictionary)
    return acronymDictionary

def getAcronymDictionaryFromPubMedXMLTraining(XMLfilename):
    tree = ET.parse(XMLfilename)
    e = tree.getroot()

    acronymDictionary = dict()
    for set in e.iter('PubmedArticleSet'):
        for article in set.iter('article'):
            for next in article.iter('front'):
                for abstract in next.iter('abstract'):
                    for abstractText in abstract.iter('p'):
                        text = abstractText.text
                        if text is not None:
                            if not type(text) == type(unicode()):
                                text = unicode(text, encoding='utf-8')
                            fixedText = unidecode.unidecode(text)
                            abstractAcronymDictionary = getAcronymDictionary(fixedText)
                            acronymDictionary = mergeDicts(acronymDictionary, abstractAcronymDictionary)
    return acronymDictionary


def getAcronymDictionaryFromPubTatorXML(XMLfilename):
    tree = ET.parse(XMLfilename)
    e = tree.getroot()
    acronymDictionary = dict()
    for collection in e.iter('collection'):
        for document in collection.iter('document'):
            for passage in document.iter('passage'):
                for abstractText in passage.iter('text'):
                    text = abstractText.text
                    if text is not None:
                        if not type(text) == type(unicode()):
                            text = unicode(text, encoding='utf-8')
                        fixedText = unidecode.unidecode(text)
                        abstractAcronymDictionary = getAcronymDictionary(fixedText)
                        acronymDictionary = mergeDicts(acronymDictionary, abstractAcronymDictionary)
    return acronymDictionary



def mergeDicts(dictionaryA, dictionaryB):
    for key in dictionaryB.keys():
        if key in dictionaryA:
            valuesB = dictionaryB[key]
            valuesA = dictionaryA[key]
            for valueB in valuesB:
                valuesA.add(valueB)
            dictionaryA[key] = valuesA
    dict = dictionaryB.copy()
    dict.update(dictionaryA)
    return dict
