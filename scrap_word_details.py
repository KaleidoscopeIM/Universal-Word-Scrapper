from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from gre_words_scripts.utils import clean_data_from_html
from gre_words_scripts.utils import nul_character_check
import json
import random

google_json_object = {}
vocab_json_object = {}
collin_json_object = {}
marrian_json_object = {}
your_dictionary_json_object = {}
header = {}

collin_data = None
google_data = None
marrian_data = None
vocabulary_data = None
your_dictionary_data = None
word_list_file = None


def initialize_variables(directive):

    if directive == "OPEN":
        global header, word_list_file, collin_data, google_data, marrian_data, vocabulary_data, your_dictionary_data, google_json_object, vocab_json_object, collin_json_object, marrian_json_object, your_dictionary_json_object
        collin_data = open("D:\Video Work Area\GRE WORDS APP\data\scrapped\collin_data.json", "r+")
        google_data = open("D:\Video Work Area\GRE WORDS APP\data\scrapped\google_data.json", "r+")
        marrian_data = open("D:\Video Work Area\GRE WORDS APP\data\scrapped\marrian_data.json", "r+")
        vocabulary_data = open("D:\Video Work Area\GRE WORDS APP\data\scrapped\Vocabulary_data.json", "r+")
        your_dictionary_data = open("D:\Video Work Area\GRE WORDS APP\data\scrapped\your_dictionary_data.json", "r+")

        google_json_object = json.load(google_data)["google_data"]
        vocab_json_object = json.load(vocabulary_data)["vocabulary_data"]
        collin_json_object = json.load(collin_data)["collin_data"]
        marrian_json_object = json.load(marrian_data)["marrian_data"]
        your_dictionary_json_object = json.load(your_dictionary_data)["your_dictionary_data"]

        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://cssspritegenerator.com',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        ua_file = open("D:\Video Work Area\GRE WORDS APP\data\init\\user_agent.txt", "r")
        count = 1
        num = random.randint(1, 5)
        user_agent = ""
        for line in ua_file:
            if num == count:
                user_agent = line
                break
            count = count + 1
        user_agent = user_agent.replace("\n", "")
        print("user agent..:"+ user_agent)
        header["User-Agent"] = user_agent
        ua_file.close()

    if directive == "CLOSE":

        google_data.close()
        marrian_data.close()
        your_dictionary_data.close()
        vocabulary_data.close()
        collin_data.close()

    if directive == "REFRESH":

        google_json_object = json.load(google_data)["google_data"]
        vocab_json_object = json.load(vocabulary_data)["vocabulary_data"]
        collin_json_object = json.load(collin_data)["collin_data"]
        marrian_json_object = json.load(marrian_data)["marrian_data"]
        your_dictionary_json_object = json.load(your_dictionary_data)["your_dictionary_data"]


def googleScrap(googleSite,word):
    googleDictionaryObj = {}
    googleDictionaryObj["WORD"]=clean_data_from_html(word)
    googleDefineFinalSite = googleSite+word
    #print("google final site:" + googleDefineFinalSite)
    googleDictionaryObj["SITE"]=googleDefineFinalSite
    try:
        page = requests.get(googleDefineFinalSite, headers=header).text
        googleDefineSoup = BeautifulSoup(page, features="html.parser")
        googleSentene=""
        googleSentenceSkipFirst=True
        try:
            for div in googleDefineSoup.find_all(lambda tag:tag.name == 'div' and tag.get('class') == ['vk_gy']):
                if(googleSentenceSkipFirst):
                    googleSentenceSkipFirst=False
                else:
                    googleSentene += div.text
                    break
        except(IndexError,ValueError):
            googleSentene += "ga_non"
        googleDictionaryObj["SENTENCE"]=clean_data_from_html(googleSentene)

        googleSynms= ""
        removeSymnText=True
        try:
            for td in googleDefineSoup.find_all("table", {"class":"vk_tbl vk_gy"})[0].find_all('td'):
                if(removeSymnText):
                    removeSymnText=False
                else:
                    googleSynms+=td.text
                    break
        except(IndexError, ValueError):
            googleSynms += "ga_non"
        googleSynms= clean_data_from_html(googleSynms)
        googleSynms=googleSynms.split(";")[0]
        googleDictionaryObj["SYNONYMS"]=googleSynms
        #print(googleSynms)

        googleAntonm=""
        removeAntonymText=True
        try:
            for td in googleDefineSoup.find_all("table", {"class":"vk_tbl vk_gy"})[1].find_all('td'):
                if(removeAntonymText):
                    removeAntonymText=False
                else:
                    googleAntonm+=td.text
                    break
        except(IndexError,ValueError):
            googleAntonm += "ga_non"
        googleAntonm=clean_data_from_html(googleAntonm)
        googleDictionaryObj["ANTONYMS"]=googleAntonm
        #print("Google Antonyms......::::::::::::"+googleAntonm)
        #print(googleAntonm)
    except Exception as e:
        print("google connection attempt failed..host not responded with request")
        #print(googleDefineSoup.prettify())
    return googleDictionaryObj

def vocalbularySiteScrap(site, word):
        vocabularyDictionaryObj={}
        vocabularyDictionaryObj["WORD"]=word
        vocabularySiteFinalUrl=site+word
        vocabularyDictionaryObj["SITE"]=vocabularySiteFinalUrl
        #print(vocabularySiteFinalUrl)
        try:
            vocabularySiteContent=urlopen(vocabularySiteFinalUrl)
            vocabularySiteSoup=BeautifulSoup(vocabularySiteContent, features="html.parser")
            countLine=3
            counter=1
            counter=1
            vocanSiteMeaning= vocabularySiteSoup.find(lambda tag: tag.name == 'h3' and tag.get('class') == ['definition'])
            for vocabMeaningSTR in vocanSiteMeaning:
                if(countLine==counter):
                    #print(cleanDataFromHTML(vocabMeaningSTR))
                    vocabMeaningSTR=clean_data_from_html(vocabMeaningSTR)
                    break
                else:
                    counter=counter+1
        except Exception as ex:
            vocabMeaningSTR="ga_non"
        vocabularyDictionaryObj["MEANING"]=vocabMeaningSTR

        try:
            VocabularySitedescription = vocabularySiteSoup.find("meta", property="og:description")
            vocabularyDictionaryObj["ATTR1"]=(VocabularySitedescription["content"] if VocabularySitedescription else "ga_non")
            #print(VocabularySitedescription["content"] if VocabularySitedescription else "ga_non")
        except Exception as ex:
            vocabularyDictionaryObj["ATTR1"]="ga_non"

        try:
            vocabularySentence=vocabularySiteSoup.find("div", {"class": "example"}).get_text()
            vocabularyDictionaryObj["SENTENCE"]=clean_data_from_html(vocabularySentence if vocabularySentence else "ga_non")
            #print(vocabularyDictionaryObj["SENTENCE"])
        except Exception as ex:
            vocabularyDictionaryObj["SENTENCE"]="ga_non"


        vocabSynmsList=""
        try:
            vocabularySynonyms = vocabularySiteSoup.findAll("a", {"class": "word"})
            for element in vocabularySynonyms:
                vocabSynmsList+=element.text +", "
            vocabSynmsList=vocabSynmsList[:-2]
            vocabularyDictionaryObj["SYNONYMS"] = vocabSynmsList
            #print(vocabSynmsList)
        except Exception as ex:
            vocabularyDictionaryObj["SYNONYMS"] = "ga_non"

        #print(vocabularySiteSoup.prettify())

        return vocabularyDictionaryObj

def yourDictionaryScrap(site, word):

        yourDictioanryObj={}
        yourDictioanryObj["WORD"]=word
        yourDictionaryFinalURL=site+word
        yourDictioanryObj["SITE"] = yourDictionaryFinalURL
        try:
            yourDictionaryContent=urlopen(yourDictionaryFinalURL)
            yourDictionarySoup=BeautifulSoup(yourDictionaryContent, features="html.parser")
            sentenceList=[]
            yourDictionarySentences= yourDictionarySoup.find(lambda tag: tag.name == 'ul' and tag.get('class') == ['greybullets'])
            for li in yourDictionarySentences.find_all('li'):
                sentenceList.append(li.text)
            yourDictioanryObj["SENTENCE"]=sentenceList
        except Exception as ex:
            yourDictioanryObj["SENTENCE"]="ga_non"

        return yourDictioanryObj


def collinScrap(site, word):

        collinDicObj={}
        collinDicObj["WORD"] = word
        collingsDictionaryFinalURL=site+word
        collinDicObj["SITE"]=collingsDictionaryFinalURL
        collinDictionaryContent=requests.get(collingsDictionaryFinalURL, headers=header).text
        collingDictionarySoup=BeautifulSoup(collinDictionaryContent, features="html.parser")

        try:
            collingDescription=collingDictionarySoup.find_all("div",{"class":"def"})[0].text
            collingDescription=clean_data_from_html(collingDescription)
            collinDicObj["ATTR1"] = collingDescription
        except Exception as ex:
            collinDicObj["ATTR1"]="ga_non"

        return collinDicObj


def marriamwebsterScrap(site, word):
        marriamDicObj={}
        marriamDicObj["WORD"]=word
        marriamwebsterFinalSite = site + word
        marriamDicObj["SITE"]=marriamwebsterFinalSite
        marriamwebsterContent = requests.get(marriamwebsterFinalSite,headers=header).text
        marriamSoup=BeautifulSoup(marriamwebsterContent,features="html.parser")
        # print(marriamSoup.prettify())
        synm_comin= False
        antm_coming= False

        try:
            mariamSynmDiv = marriamSoup.find_all("div", {"class": "thesaurus-synonyms-module-anchor"})[0]
            pTagAll = mariamSynmDiv.findAll('p')
            for pTag in pTagAll:
                if synm_comin:
                    marriamDicObj["SYNONYMS"] = clean_data_from_html(pTag.text)
                    synm_comin = False
                if clean_data_from_html(pTag.text) == "Synonyms":
                    synm_comin = True
                if antm_coming:
                    marriamDicObj["ANTONYMS"] = clean_data_from_html(pTag.text)
                    antm_coming = False
                if clean_data_from_html(pTag.text) == "Antonyms":
                    antm_coming = True

        except Exception as ex:
                marriamDicObj["SYNONYMS"]="ga_non"
                marriamDicObj["SYNONYMS"]="ga_non"

        if "SYNONYMS" not in marriamDicObj:
            marriamDicObj["SYNONYMS"] = "ga_non"
        if "ANTONYMS" not in marriamDicObj:
            marriamDicObj["ANTONYMS"] = "ga_non"

        try:
            citeexamples = marriamSoup.find_all("div",{"class":"in-sentences"})[0]
            citespan = citeexamples.findAll('span')
            citeexamplesList=[]
            for span in citespan:
                citeexamplesList.append(clean_data_from_html(span.text))
                break
            marriamDicObj["SENTENCE"]= citeexamplesList
        except Exception as ex:
            marriamDicObj["SENTENCE"]="ga_non"
        return marriamDicObj


def end_close_json(data, file, word, objlist, start_string):

    already_scrapped = False
    for obj in objlist:
        if obj["WORD"] == word:
            already_scrapped = True
            print(word + " already scrapped.. updating values now for..:"+start_string)
            for key in data:
                obj[key] = data[key]
            break

    if already_scrapped:
        file.seek(0)
        file.truncate()
        file.write("{\""+start_string+"\":")
        json.dump(objlist, file)
        file.write("}")
        file.flush()
        file.close()

    else:
        file.seek((file.tell())-2)
        file.write(",")
        json.dump(data, file)
        file.write("]}")
        file.flush()
        file.close()


def scrap_word_main(word):

    initialize_variables("OPEN")
    googleData = googleScrap("https://www.google.com/search?q=define%3A+", word)
    print("google data..:"+ str(googleData))
    vocabData = vocalbularySiteScrap("https://www.vocabulary.com/dictionary/", word)
    print("Vocab data..:"+str(vocabData))
    yourDictionaryData = yourDictionaryScrap("http://www.yourdictionary.com/", word)
    print("your dict data..:"+str(yourDictionaryData))
    collingDicData = collinScrap("https://www.collinsdictionary.com/dictionary/english/", word)
    print("Collin data..:"+str(collingDicData))

    marriamDicData = marriamwebsterScrap("https://www.merriam-webster.com/dictionary/", word)
    print("marriam data..:"+str(marriamDicData))

    end_close_json(googleData, google_data, word, google_json_object, "google_data")
    end_close_json(vocabData, vocabulary_data, word, vocab_json_object, "vocabulary_data")
    end_close_json(yourDictionaryData, your_dictionary_data, word, your_dictionary_json_object, "your_dictionary_data")
    end_close_json(collingDicData, collin_data, word, collin_json_object, "collin_data")
    end_close_json(marriamDicData, marrian_data, word, marrian_json_object, "marrian_data")

    nul_character_check()

