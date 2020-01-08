import json
import shutil
import os

def clean_data_from_html(rich_text):
    out = rich_text
    out = out.replace("\n", "")
    out = out.replace(":", "")
    out = out.replace(";", "")
    out = out.replace("\"", "")
    out = out.replace("“", "")
    out = out.replace("”", "")
    out = out.replace("\t", "")
    out = out.replace("\r", "")
    out = out.replace("  ", "")
    out= out.lstrip()
    return out


def nul_character_check():

    file_list = {"D:\Video Work Area\GRE WORDS APP\data\scrapped\collin_data.json",
                 "D:\Video Work Area\GRE WORDS APP\data\scrapped\google_data.json",
                 "D:\Video Work Area\GRE WORDS APP\data\scrapped\marrian_data.json",
                 "D:\Video Work Area\GRE WORDS APP\data\scrapped\Vocabulary_data.json",
                 "D:\Video Work Area\GRE WORDS APP\data\scrapped\your_dictionary_data.json",
                 "D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json",
                 "D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json"}

    for f in file_list:
        file = open(f, "rb+")
        byte = file.read()
        nul_bytes = byte.count(b'\x00')
        if nul_bytes > 0:
            byte = byte.replace(b'\x00', b'')
            print(" --------------->   Attention total = " + str(nul_bytes) + " NUL byte found in file...: " + f)
            file.seek(0)
            file.truncate()
            file.write(byte)
            file.flush()
        file.close()

def init_files():
    shutil.copy("D:\Video Work Area\GRE WORDS APP\data\init\collin_data.json",
                "D:\Video Work Area\GRE WORDS APP\data\scrapped\collin_data.json")
    shutil.copy("D:\Video Work Area\GRE WORDS APP\data\init\google_data.json",
                "D:\Video Work Area\GRE WORDS APP\data\scrapped\google_data.json")
    shutil.copy("D:\Video Work Area\GRE WORDS APP\data\init\marrian_data.json",
                "D:\Video Work Area\GRE WORDS APP\data\scrapped\marrian_data.json")
    shutil.copy("D:\Video Work Area\GRE WORDS APP\data\init\Vocabulary_data.json",
                "D:\Video Work Area\GRE WORDS APP\data\scrapped\Vocabulary_data.json")
    shutil.copy("D:\Video Work Area\GRE WORDS APP\data\init\your_dictionary_data.json",
                "D:\Video Work Area\GRE WORDS APP\data\scrapped\your_dictionary_data.json")
    shutil.copy("D:\Video Work Area\GRE WORDS APP\data\init\WordsList.json",
                "D:\Video Work Area\GRE WORDS APP\data\scrapped\WordsList.json")
    shutil.copy("D:\Video Work Area\GRE WORDS APP\data\init\WordsList.json",
                "D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json")

    image_temp_dir = r"D:\Video Work Area\GRE WORDS APP\data\scrapped\scrapped_images\\"
    for objs in os.listdir(image_temp_dir):
        path = image_temp_dir+objs
        if os.path.isfile(path):
            os.unlink(path)
        else:
            shutil.rmtree(path)

    dst_image_dir = r"D:\Video Work Area\GRE WORDS APP\data\production\images\\"
    for objs in os.listdir(dst_image_dir):
        path= dst_image_dir + objs
        if os.path.isfile(path):
            os.unlink(path)
        else:
            shutil.rmtree(path)


def run_diagnostics():
    print(">>>>>>>>>>>>>>>>>>>>>> Starting data diagnostic ")
    log_file = open("D:\Video Work Area\GRE WORDS APP\data\logs\diagnostics.log", "a+")
    log_file.seek(0)
    log_file.truncate()
    words_list_file = open("D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json", "r")
    words_list_objs = json.load(words_list_file)["words"]

    barron333_not_proceed_yet = []
    barron333_words_list_txt = open("D:\Video Work Area\GRE WORDS APP\data\Barron333WordsList.txt", "r")
    for y in barron333_words_list_txt:
        y = clean_data_from_html(y)
        barron333_not_proceed_yet.append(y)
    barron333_words_list_txt.seek(0)

    barron800_not_proceed_yet = []
    barron800_words_list_txt = open("D:\Video Work Area\GRE WORDS APP\data\Barron800WordsList.txt", "r")
    for y in barron800_words_list_txt:
        y = clean_data_from_html(y)
        barron800_not_proceed_yet.append(y)
    barron800_words_list_txt.seek(0)

    for obj in words_list_objs:
        word = obj["WORD"]
        wid = obj["ID"]
        if obj["TYPE"] is None or obj["TYPE"] == "" or obj["TYPE"] == "ga_non":
            message = word + " has no type"
            log_file.write(message)
            print(message)
        if obj["MEANING"] is None or obj["MEANING"] == "" or obj["MEANING"] == "ga_non":
            message = word + " has no meaning"
            log_file.write(message)
            print(message)
        if obj["SENTENCE"] is None or obj["SENTENCE"] == "" or obj["SENTENCE"] == "ga_non":
            message = word + " has no sentence"
            log_file.write(message)
            print(message)
        if obj["SYNONYMS"] is None or obj["SYNONYMS"] == "" or obj["SYNONYMS"] == "ga_non":
            message = word + " has no synonyms"
            log_file.write(message)
            print(message)
        if obj["ANTONYMS"] is None or obj["ANTONYMS"] == "" or obj["ANTONYMS"] == "ga_non":
            message = word + " has no antonyms"
            log_file.write(message)
            # print(message)
        if obj["ATTR1"] is None or obj["ATTR1"] == "" or obj["ATTR1"] == "ga_non":
            message = word + " has no attr1"
            log_file.write(message)
            print(message)

        image_temp_dir = r"D:\Video Work Area\GRE WORDS APP\data\scrapped\scrapped_images\\" + word + "\\"
        if not os.path.exists(image_temp_dir):
            print(word + " had no scrapped images")
            log_file.write(word + " had no scrapped images")
        elif len(os.listdir(image_temp_dir)) == 0:
            print(word + "has no scrapped images")
            log_file.write(word + "has no scrapped images")
        else:
            img_list = os.listdir(image_temp_dir)
            if len(img_list) < 3:
                print(word + " has less then 3 images")
                log_file.write(word + " has less then 3 images")
            dst_img_list = os.listdir(r"D:\Video Work Area\GRE WORDS APP\data\production\images\\")
            for img_scrapped in img_list:
                src_img_name = str(img_scrapped)
                found = False
                for img_dst in dst_img_list:
                    dst_img_name = str(img_dst)
                    if src_img_name == dst_img_name:
                        found = True
                        break
                if found is False:
                    print("Warning - scrapped image not copied in image directory.    image name :"+src_img_name)
                    log_file.write("Warning - scrapped image not copied in image directory.  image name :"+src_img_name)

        barron333_json = open("D:\Video Work Area\GRE WORDS APP\data\production\Barron333.json", "r")
        barron333_json_obj = json.load(barron333_json)["BARRON333"]
        is333_barron_word = False
        for x in barron333_words_list_txt:
            x = clean_data_from_html(x)
            if x == word:
                is333_barron_word = True
                break
        barron333_words_list_txt.seek(0)

        if is333_barron_word is True:
            barron333_not_proceed_yet.remove(word)
            found = False
            for barron333obj in barron333_json_obj:
                if wid == barron333obj["BARRONID"]:
                    found = True
            if found is False:
                print(word + " has not been added in barron 333 json file")
                log_file.write(word + " has not been added in barron 333 json file")
        barron333_json.close()

        barron800_json = open("D:\Video Work Area\GRE WORDS APP\data\production\Barron800.json", "r")
        barron800_json_objs = json.load(barron800_json)["BARRON800"]
        is_barron800_word = False
        for x in barron800_words_list_txt:
            x = clean_data_from_html(x)
            if x == word:
                is_barron800_word = True
                break
        barron800_words_list_txt.seek(0)

        if is_barron800_word is True:
            barron800_not_proceed_yet.remove(word)
            found = False
            for barron800obj in barron800_json_objs:
                if wid == barron800obj["BARRONID"]:
                    found = True
            if found is False:
                print(word + " has not been added in barron 800 json file")
                log_file.write(word + " has not been added in barron 800 json file")
        barron800_json.close()

    if len(barron333_not_proceed_yet) != 0:
        print("barron 333 words not scrapped yet..:" + str(len(barron333_not_proceed_yet)))
        print(barron333_not_proceed_yet)
    else:
        print("all barron 333 words scrapped")
    if len(barron800_not_proceed_yet) != 0:
        print("barron 800 words not scrapped yet..:" + str(len(barron800_not_proceed_yet)))
        print(barron800_not_proceed_yet)
    else:
        print("all barron 800 words scrapped")

    log_file.flush()
    log_file.close()
    barron333_words_list_txt.close()
    barron800_words_list_txt.close()


def sort_json():

    print("sorting json..:")
    word_list_src = open(r"D:\Video Work Area\GRE WORDS APP\data\scrapped\WordsList.json", "r+")
    word_list_dst = open(r"D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json", "w")

    file_obj = json.load(word_list_src)["words"]
    word_list = []
    for obj in file_obj:
        word_list.append(obj["WORD"])
    word_list = sorted(word_list)
    word_id = 1
    word_string = "{\"words\":["
    for word in word_list:
        for obj in file_obj:
            if word == obj["WORD"] and obj["WORD"] != "":
                word_string = word_string + "{\"ID\":" + str(word_id) + ","
                word_string = word_string + "\"WORD\":\"" + word + "\","
                word_string = word_string + "\"TYPE\":\"" + obj["TYPE"] + "\","
                word_string = word_string + "\"MEANING\":\"" + obj["MEANING"] + "\","
                word_string = word_string + "\"SENTENCE\":\"" + obj["SENTENCE"] + "\","
                word_string = word_string + "\"SYNONYMS\":\"" + obj["SYNONYMS"] + "\","
                word_string = word_string + "\"ANTONYMS\":\"" + obj["ANTONYMS"] + "\","
                word_string = word_string + "\"ATTR1\":\"" + obj["ATTR1"] + "\","
                word_string = word_string + "\"LINK\":\"\","
                word_string = word_string + "\"ATTR2\":\"\"},"
                word_id = word_id + 1
                break
    word_string = word_string[:-1]
    word_string = word_string + "]}"
    word_list_dst.write(word_string)
    print("sorted string word list json..:"+ word_string)
    word_list_dst.flush()
    word_list_dst.close()
    word_list_src.close()
