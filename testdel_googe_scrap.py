from PyDictionary import PyDictionary
import json
from gre_words_scripts.utils import clean_data_from_html
import random

dictionary = PyDictionary()

google_json_object = {}
vocab_json_object = {}
collin_json_object = {}
marrian_json_object = {}
your_dictionary_json_object = {}

collin_data = None
google_data = None
marrian_data = None
vocabulary_data = None
your_dictionary_data = None


def initialize_variables(directive):

    if directive == "OPEN":
        global collin_data, google_data, marrian_data, vocabulary_data, your_dictionary_data, google_json_object, vocab_json_object, collin_json_object, marrian_json_object, your_dictionary_json_object
        collin_data = open("D:\Video Work Area\GRE WORDS APP\data\\beta_version\scrapper\collin_data.json", "r+")
        google_data = open("D:\Video Work Area\GRE WORDS APP\data\\beta_version\scrapper\google_data.json", "r+")
        marrian_data = open("D:\Video Work Area\GRE WORDS APP\data\\beta_version\scrapper\marrian_data.json", "r+")
        vocabulary_data = open("D:\Video Work Area\GRE WORDS APP\data\\beta_version\scrapper\Vocabulary_data.json", "r+")
        your_dictionary_data = open("D:\Video Work Area\GRE WORDS APP\data\\beta_version\scrapper\your_dictionary_data.json", "r+")

        google_json_object = json.load(google_data)["google_data"]
        vocab_json_object = json.load(vocabulary_data)["vocabulary_data"]
        collin_json_object = json.load(collin_data)["collin_data"]
        marrian_json_object = json.load(marrian_data)["marrian_data"]
        your_dictionary_json_object = json.load(your_dictionary_data)["your_dictionary_data"]

    if directive == "CLOSE":

        google_data.close()
        marrian_data.close()
        your_dictionary_data.close()
        vocabulary_data.close()
        collin_data.close()

def get_type(word_input):

    dict_meaning = dictionary.meaning(word_input)
    if dict_meaning is None:
        print("error this word not found in pyDictionary.." + word_input)
        return ""
    if "Verb" in dict_meaning:
        return "Verb"
    elif "Noun" in dict_meaning:
        return "Noun"
    elif "Adjective" in dict_meaning:
        return "Adjective"
    else:
        print("word meaning not found quitting.." + word_input)
        type_in = ""
        return type_in


def get_meaning(word_input):

    found = False
    meaning = ""
    for obj in vocab_json_object:
        vocab_word = clean_data_from_html(obj["WORD"])
        if vocab_word == word_input:
            found = True
            meaning = obj["MEANING"]
            break

    if found:
        print("meaning found in vocab dictionary : " + meaning)
        return meaning
    else:
        dict_meaning = dictionary.meaning(word_input)
        if dict_meaning is not None:
            for key in dict_meaning:
                for m in dict_meaning.get(key):
                    found = True
                    #meaning = meaning+m+" OR "
                    meaning = m
                    break
    if found:
        # meaning=meaning[:-4]
        print("meaning found in pyDictionary..:" + meaning)
        return meaning
    else:
        print("error.. meaning not found for...." + word_input)
        return ""


def get_sentence(word_input):

    found=False
    sentence=""
    for obj in google_json_object:
        google_word = clean_data_from_html(obj["WORD"])
        if google_word == word_input:
            if obj["SENTENCE"] != "" and obj["SENTENCE"] != "ga_non" and obj["SENTENCE"] is not None and obj["SENTENCE"] != "":
                sentence = obj["SENTENCE"]
                found = True
            break
    if found:
        print("sentence from google data..:"+sentence)
        return sentence
    else:
        for obj in your_dictionary_json_object:
            your_dict_word=clean_data_from_html(obj["WORD"])
            if your_dict_word == word_input:
                if obj["SENTENCE"] != "" and obj["SENTENCE"] != "ga_non" and obj["SENTENCE"] is not None and obj["SENTENCE"] != "":
                    sentence = obj["SENTENCE"][0]
                    found = True
                break
    if found:
        print("sentence from your dictionary.."+ sentence)
        return sentence
    else:
        print("sentence not found for word....: "+word_input)
        return ""


def get_synonyms(word_input):
    synonyms = ""
    found=False
    for obj in google_json_object:
        google_word = clean_data_from_html(obj["WORD"])
        if google_word == word_input:
            if obj["SYNONYMS"] != "" and obj["SYNONYMS"] != "ga_non" and obj["SYNONYMS"] is not None and obj["SYNONYMS"] != "":
                synonyms = obj["SYNONYMS"]
                found = True
            break
    if found:
        print("synonyms from google..:"+ synonyms)
        return synonyms
    else:
        for obj in marrian_json_object:
            marrian_word=obj["WORD"]
            if marrian_word == word_input:
                if obj["SYNONYMS"] != "" and obj["SYNONYMS"] != "ga_non" and obj["SYNONYMS"] is not None and obj["SYNONYMS"] != "":
                    synonyms = obj["SYNONYMS"]
                    found = True
                break
    if found:
        print("synonyms from marriam dictionary..:" + synonyms)
        return synonyms
    else:
        for obj in vocab_json_object:
            vocab_word = obj["WORD"]
            if vocab_word == word_input:
                if obj["SYNONYMS"] != "" and obj["SYNONYMS"] != "ga_non" and obj["SYNONYMS"] is not None and obj["SYNONYMS"] != "":
                    synonyms = obj["SYNONYMS"]
                    found = True
                break
    if found:
        print("synonyms from vocab dictionary..:" + synonyms)
        return synonyms
    else:
        print("not found for ...:"+word_input)
        return synonyms


def get_antonyms(word_input):
    antonyms = ""
    found = False
    for obj in google_json_object:
        google_word = clean_data_from_html(obj["WORD"])
        if google_word == word_input:
            if obj["ANTONYMS"] != "" and obj["ANTONYMS"] != "ga_non" and obj["ANTONYMS"] is not None and obj["ANTONYMS"] != "":
                antonyms = obj["ANTONYMS"]
                found = True
            break
    if found:
        print("antonyms from google..:" + antonyms)
        return antonyms
    else:
        for obj in marrian_json_object:
            marrian_word = obj["WORD"]
            if marrian_word == word_input:
                if obj["ANTONYMS"] != "" and obj["ANTONYMS"] != "ga_non" and obj["ANTONYMS"] is not None and obj["ANTONYMS"] != "":
                    antonyms = obj["ANTONYMS"]
                    found = True
                break
    if found:
        print("antonyms from marriam dictionary..:" + antonyms)
        return antonyms
    else:
        print("Antonyms not found for ...:" + word_input+".... returning empty")
        return antonyms


def get_attr1(word_input):
    attr1=""
    found=False
    for obj in vocab_json_object:
        vocab_word = obj["WORD"]
        if vocab_word == word_input:
            if obj["ATTR1"] != "" and obj["ATTR1"] != "ga_non" and obj["ATTR1"] is not None and obj["ATTR1"] != "":
                attr1 = obj["ATTR1"]
                found = True
            break
    if found:
        print("attr1 from vocab..:"+attr1)
        return attr1
    else:
        for obj in collin_json_object:
            collin_word = obj["WORD"]
            if collin_word == word_input:
                if obj["ATTR1"] != "" and obj["ATTR1"] != "ga_non" and obj["ATTR1"] is not None and obj["ATTR1"] != "":
                    attr1 = obj["ATTR1"]
                    found = True
                break
    if found:
        print("attr1 from collin..:" + attr1)
        return attr1
    else:
        print("attr1 not found for.."+word_input)
        return attr1


def write_with_remove_redundancy(word_string, word):

    file = open("D:\Video Work Area\GRE WORDS APP\data\\beta_version\\temp\WordsList.json", "rb+")
    byte = file.read()
    nul_bytes = byte.count(b'\x00')
    if nul_bytes > 0:
        byte = byte.replace(b'\x00', b'')
        print(" --------------->   Attention total = " + str(nul_bytes) + " NUL byte found in file...: ")
        file.seek(0)
        file.truncate()
        file.write(byte)
        file.flush()
    file.close()
    '''redundant = False
    redundant_count = 1
    all_obj = json.load(file)["words"]
    for obj in all_obj:
        if word == obj["WORD"]:
            redundant = True
            if redundant_count == 1:
                print("Word details was added in file.. updating values in temp word list file")
                obj["TYPE"] = get_type(word)
                obj["MEANING"] = get_meaning(word)
                obj["SENTENCE"] = clean_data_from_html(get_sentence(word))
                obj["SYNONYMS"] = get_synonyms(word)
                obj["ANTONYMS"] = get_antonyms(word)
                obj["ATTR1"] = clean_data_from_html(get_attr1(word))
                redundant_count = redundant_count+1
            else:
                print("Found multiple entries in temp word details .. updating values to empty all data.....total redundancy..:" + str(redundant_count))
                obj["WORD"] = ""
                obj["TYPE"] = ""
                obj["MEANING"] = ""
                obj["SENTENCE"] = ""
                obj["SYNONYMS"] = ""
                obj["ANTONYMS"] = ""
                obj["ATTR1"] = ""


'''

def fetch_word_details():

    initialize_variables("OPEN")
    word = "Bedizen"
    find_id = random.randint(10000, 20000)
    final_type = get_type(word)
    final_meaning = get_meaning(word)
    final_sentence = clean_data_from_html(get_sentence(word))
    final_synonyms = get_synonyms(word)
    final_antonyms = get_antonyms(word)
    final_attr1 = clean_data_from_html(get_attr1(word))

    word_string = ""
    word_string = word_string+"{\"ID\":"+str(find_id)+","
    word_string = word_string+"\"WORD\":\""+word+"\","
    word_string = word_string + "\"TYPE\":\"" + final_type + "\","
    word_string = word_string + "\"MEANING\":\"" + final_meaning + "\","
    word_string = word_string + "\"SENTENCE\":\"" + final_sentence + "\","
    word_string = word_string + "\"SYNONYMS\":\"" + final_synonyms + "\","
    word_string = word_string + "\"ANTONYMS\":\"" + final_antonyms + "\","
    word_string = word_string + "\"ATTR1\":\"" + final_attr1 + "\","
    word_string = word_string + "\"LINK\":\"\","
    word_string = word_string + "\"ATTR2\":\"\"}"

    print("final word string..:"+word_string)

    write_with_remove_redundancy(word_string,word)

    initialize_variables("CLOSE")


fetch_word_details()