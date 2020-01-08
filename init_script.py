import json
from gre_words_scripts.utils import clean_data_from_html
from gre_words_scripts.scrap_word_details import scrap_word_main
from gre_words_scripts.find_word_details import fetch_word_details
from gre_words_scripts.utils import sort_json
from gre_words_scripts.scrap_images import scrap_google_images
from gre_words_scripts.scrap_images import scrap_common_images
from gre_words_scripts.json_creator import json_creator_barrons
from gre_words_scripts.scrap_images import shuffle_images
from gre_words_scripts.scrap_images import optimize_images
from gre_words_scripts.utils import run_diagnostics
from gre_words_scripts.utils import init_files
import time
import random

all_words = open("D:\Video Work Area\GRE WORDS APP\data\\all_words.txt", "r")
words_list = open("D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json", "r")

# init_files()  # >>>>>>>>>>>> reset values most imp method <<<<<<<<<<<<<<<<<

words_list_dict = json.load(words_list)["words"]

count = 1
for word in all_words:

    word = clean_data_from_html(word)

    count = count+1

    exists = False
    for word_obj in words_list_dict:
        if word_obj["WORD"] == word:
            exists = True
            break
    if exists is False:
        print("\n\n\n     >>>>>>>>>>>>>>>>>>>>>>>>>>>      Processing ..: " + word + "        ::" + str(count) +
              "            Percent Done..:"
              + str((int((count / 801) * 100))) + "%   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n")

        # get word details and store them in scrapper folder
        scrap_word_main(word)
        # get appropriate word details and store them in word list at temp location /temp/WordList.json
        fetch_word_details(word)


all_words.close()
words_list.close()

# pickup temp folder word list json then sort it and write to root folder WordList json
# if word is empty it will not write in root word list
sort_json()

# to create 333 and 800 json using word list json
json_creator_barrons()

# using production word list scrapping images from other sites
scrap_common_images()

# using word list pick images from scrapped_images and copy then in production/images and create data map json in root
shuffle_images()

# to reduce the size of image and compress them
optimize_images()

# run_diagnostics()
print(">>>>>>>>>>>>> DONE ")





