import json
from selenium import webdriver
import requests
from gre_words_scripts.error_handler import handle_error
from gre_words_scripts.error_handler import handle_logging
import time
import os
import shutil
import random
import tinify
from PIL import Image

image_temp_dir = r"D:\Video Work Area\GRE WORDS APP\data\scrapped\scrapped_images\\"
dst_image_dir = r"D:\Video Work Area\GRE WORDS APP\data\production\images\\"


def get_random_user_agent():
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
    print("random user agent..:" + user_agent)
    ua_file.close()
    return user_agent


def driver_get(url, driver):
    waiting_for_site = True
    attempt = 1
    while waiting_for_site:
        try:
            driver.get(url)
            waiting_for_site = False
        except Exception as e:
            attempt = attempt + 1
            print("Error..retrying after 10S")
            time.sleep(10)
        if attempt == 3:
            break


def shuffle_images():

    image_dirs = os.listdir(image_temp_dir)
    image_data_map = open("D:\Video Work Area\GRE WORDS APP\data\scrapped\DataMap.json", "w")

    filein = open("D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json", "r")
    filein_obj = json.load(filein)["words"]

    dst_img_list = os.listdir(dst_image_dir)

    # clean destination folder
    # shutil.rmtree(dst_image_dir)
    # os.mkdir(dst_image_dir)

    tinify.key = "K1vHKBolqhWCjYOqOOhPN9UjidqvGceN"

    img_string = "{\"FDATA\":["

    for obj in filein_obj:
        word = obj["WORD"].lower()
        img_string = img_string + "{\"MAPID\":" + str(obj["ID"]) + ","
        already_copied = False
        for img_name in dst_img_list:
            if word in img_name:
                already_copied = True
                img_string = img_string + "\"" + str(img_name) + "\"" + ":" + "\"" + str(img_name) + "\"" + ","

        if already_copied:
            img_string = img_string[:-1]
            img_string = img_string + "},"

        else:
            print(">>> shuffling images for.. : >>>>>>>>>>  " + word + "  <<<<<<<<<")
            for dir_name in image_dirs:
                if str(dir_name) == word:
                    # print("\n copying images for......: " + word)
                    src_image_dir = image_temp_dir + str(dir_name) + "\\"
                    images = os.listdir(src_image_dir)
                    img_count = 1
                    for img in images:
                        src_img = src_image_dir + str(img)
                        dst_img = dst_image_dir + str(img)
                        if '.gif' in str(img) or 'google' in str(img):
                            continue
                        else:
                            shutil.copy(src_img, dst_img)
                            print("Copying image... :" + src_img)
                            img_string = img_string + "\"" + str(img) + "\"" + ":" + "\"" + str(img) + "\"" + ","
                            img_count = img_count + 1
                            if img_count == 6:
                                break

                    if img_count < 2:  # if images are not enough then copy google images
                        for img in images:
                            src_img = src_image_dir + str(img)
                            dst_img = dst_image_dir + str(img)
                            if 'google' in str(img):
                                shutil.copy(src_img, dst_img)
                                print("Copying google image... :" + src_img)
                                img_string = img_string + "\"" + str(img) + "\"" + ":" + "\"" + str(img) + "\"" + ","
                                img_count = img_count + 1
                                if img_count == 6:
                                    break

                    img_string = img_string[:-1]
                    img_string = img_string + "},"
                    break

    img_string = img_string[:-1]
    img_string = img_string + "]}"
    image_data_map . write(img_string)
    image_data_map.flush()
    image_data_map.close()
    filein.close()

    shutil.copy("D:\Video Work Area\GRE WORDS APP\data\scrapped\DataMap.json",
                "D:\Video Work Area\GRE WORDS APP\data\production\DataMap.json")


def optimize_images():

    words_list = open("D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json", "r")
    words_list_dict = json.load(words_list)["words"]
    image_dir = r"D:\Video Work Area\GRE WORDS APP\data\production\images\\"

    scrapped_data_map = open("D:\Video Work Area\GRE WORDS APP\data\scrapped\DataMap.json", "r")
    scrapped_dm_obj = json.load(scrapped_data_map)["FDATA"]
    production_data_map = open("D:\Video Work Area\GRE WORDS APP\data\production\DataMap.json", "w")

    prod_dm_str = "{\"FDATA\":["

    for obj in words_list_dict:
        for obj1 in scrapped_dm_obj:
            if obj["ID"] == obj1["MAPID"]:

                for img in obj1.keys():
                    if img == 'MAPID':
                        prod_dm_str = prod_dm_str + "{\"MAPID\":" + str(obj["ID"]) + ","
                        continue

                    img_path = image_dir + str(img)
                    # print("processing image ..:" + img_path)
                    try:
                        if '.gif' in img_path and os.path.exists(img_path):
                            prod_dm_str = prod_dm_str + "\"" + str(img) + "\"" + ":" + "\"" + str(img) + "\"" + ","
                            continue
                        processing_img = Image.open(img_path)
                        if processing_img.size[0] > 620:
                            print("Need width scale..:" + img_path + "        size..:" + str(processing_img.size))
                            print("size before scale..:" + str(os.stat(img_path).st_size))
                            width = 620
                            wpercent = (width / float(processing_img.size[0]))
                            height = int((processing_img.size[1]) * wpercent)
                            processing_img = processing_img.resize((width, height), Image.ANTIALIAS)
                            processing_img.save(img_path, optimize=True, quality=50)
                            print("size after scale..:" + str(os.stat(img_path).st_size))
                        if processing_img.size[1] > 420:
                            print("Need height scale..:" + img_path + "        size..:" + str(processing_img.size))
                            print("size before scale..:" + str(os.stat(img_path).st_size))
                            height = 420
                            hpercent = (height / float(processing_img.size[1]))
                            width = int((processing_img.size[0]) * hpercent)
                            processing_img = processing_img.resize((width, height), Image.ANTIALIAS)
                            processing_img.save(img_path, optimize=True, quality=50)
                            print("size after scale..:" + str(os.stat(img_path).st_size))
                        if (os.path.getsize(img_path)) > 130000:
                            print("processing large size image..:" + img_path + "    size ....: " + str(os.path.getsize(img_path)))
                            tinify.from_file(img_path).to_file(img_path)

                        prod_dm_str = prod_dm_str + "\"" + str(img) + "\"" + ":" + "\"" + str(img) + "\"" + ","

                    except Exception as e:
                        print("removing invalid Image..:" + img_path)
                        try:
                            os.remove(img_path)
                        except Exception as e:
                            print("Unable to delete so making it invalid file..:" + img_path)
                            del_file = open(img_path, 'w')
                            del_file.close()
                prod_dm_str = prod_dm_str[:-1]
                prod_dm_str = prod_dm_str + "},"

    prod_dm_str = prod_dm_str[:-1]
    prod_dm_str = prod_dm_str + "]}"
    production_data_map.write(prod_dm_str)
    production_data_map.flush()

    all_images = os.listdir(image_dir)
    for img in all_images:
        img_path = image_dir + str(img)
        try:
            Image.open(img_path)
        except Exception as e:

            print("cleaning invalid image...:" + img_path)
            try:
                os.remove(img_path)
            except Exception as e:
                print("could not delete the file..:" + img_path)
                print(e)

    shutil.copy("D:\Video Work Area\GRE WORDS APP\data\production\DataMap.json",
                "D:\Video Work Area\GRE WORDS APP\data\scrapped\DataMap.json")
    words_list.close()
    scrapped_data_map.close()
    production_data_map.close()


def write_raw_ing_file(raw_img, img_path):
    file = open(img_path, "wb+")
    file.write(raw_img)
    file.flush()
    file.close()


def scrap_google_images(word, driver, hdr, img_count):

    google_img_url_set = google_urls_scrap(word, driver)
    trusted_url = intelli_g(google_img_url_set)

    for download_url in trusted_url:

        try:
            raw_img = requests.get(download_url, headers=hdr).content
            image_name = "google_" + word + str(img_count) + get_img_type(download_url)
            image_path = image_temp_dir + word + "\\" + image_name
            print("google image downloading at path..:" + image_path)
            write_raw_ing_file(raw_img, image_path)
            img_count = img_count + 1
            details = {"word": word, "img_name": image_name, "image_url": download_url}
            handle_logging("IMAGE_DOWNLOAD_SUCCESS", details)
        except Exception as e:
            print(download_url)
            print(e)
            details = {"word": word, "img_name": image_name, "word_url": "google", "image_url": download_url}
            handle_error("IMAGE_DOWNLOAD_ERROR", details)
        if img_count == 8:
            break


def scrap_get_word_img(word, driver, hdr):
    url = "http://getwords.com/results/" + word + "/"
    print("get word url ...:" + word + "   :: " + url)
    driver_get(url, driver)
    # all_elem = driver.find_element_by_xpath("//*")
    # print(all_elem.get_attribute("outerHTML"))
    try:
        xpath = "//div[@class=\"definition\"]//img"
        img_url = driver.find_elements_by_xpath(xpath)
        count = 1
        for img in img_url:
            img_url = img.get_attribute('src')
            print("get word image url " + str(count) + " ...:" + str(img_url))
            raw_img = requests.get(img_url, headers=hdr).content
            img_path = image_temp_dir + word + "\\" + "get_word_" + word + str(count) + get_img_type(img_url)
            print("get word image path..:"+img_path)
            write_raw_ing_file(raw_img, img_path)
            count = count+1

    except Exception as e:
        print("Couldn't download image from get word for ..:" + word)
        print(e)


def scrap_word_pandit_img(word, driver, hdr):
    url = "https://wordpandit.com/" + word + "/"
    print("word pandit...:" + word + "   :: " + url)
    driver_get(url, driver)
    # all_elem = driver.find_element_by_xpath("//*")
    # print(all_elem.get_attribute("outerHTML"))
    try:
        xpath = "//img[@title = '" + word + "']"
        try_upper = False
        try:
            img_url = driver.find_elements_by_xpath("//img[@title = '" + word + "']")[0].get_property('src')
        except Exception as e:
            try_upper = True
            print("trying to get URL using lower case word")
        if try_upper:
            img_url = driver.find_elements_by_xpath("//img[@title = '" + word.capitalize() + "']")[0].get_property('src')
        print("word pandit image url..:" + img_url)
        raw_img = requests.get(img_url, headers=hdr).content
        img_path = image_temp_dir + word + "\\" + "word_pandit_" + word + get_img_type(img_url)
        print("word pandit image path..:"+img_path)
        write_raw_ing_file(raw_img, img_path)

    except Exception as e:
        print("Couldn't download image from world pandit for ..:"+ word)
        print(e)


def scrap_spin_fold_img(word, driver, hdr):
    url = "http://www.spinfold.com/" + word + "-meaning/"
    print("spin fold...:" + word + "   :: " + url)
    driver_get(url, driver)
    # all_elem = driver.find_element_by_xpath("//*")
    # print(all_elem.get_attribute("outerHTML"))

    try:
        img_url = driver.find_elements_by_xpath("//meta[@property = 'og:image']")[0].get_property('content')
        print("spin fold image url..:" + img_url)
        raw_img = requests.get(img_url, headers=hdr).content
        img_path = image_temp_dir + word + "\\" + "spin_fold_" + word + get_img_type(img_url)
        print("spin fold image path..:"+img_path)
        write_raw_ing_file(raw_img, img_path)

    except Exception as e:
        print("Couldn't download image from spin fold for ..:"+ word)
        print(e)


def scrap_daily_vocab_img(word, driver, hdr):

    try:
        url = "http://dailyvocab.com/photos/" + word + "/"
        print("daily vocab...:" + word + "   :: " + url)
        driver_get(url, driver)
        check_article = False
        img_url = ''
        try:
            img_url = driver.find_elements_by_xpath("//meta[@name = 'twitter:image']")[0].get_property('content')
        except Exception as e:
            print("Checking in article")
            check_article = True

        if check_article:
            url = "http://dailyvocab.com/articles/" + word + "/"
            print("daily vocab url changed...:" + word + "   :: " + url)
            driver_get(url, driver)
            img_url = driver.find_elements_by_xpath("//meta[@name = 'twitter:image']")[0].get_property('content')

        print("daily vocab image url..:" + img_url)
        raw_img = requests.get(img_url, headers=hdr).content
        img_path = image_temp_dir + word + "\\" + "daily_vocab_" + word + get_img_type(img_url)
        print("daily vocab image path..:"+img_path)
        write_raw_ing_file(raw_img, img_path)

    except Exception as e:
        print("Couldn't download image from daily vocab for ..:"+word)
        print(e)


def scrap_working_school(word, driver, hdr):
    url = "https://workschoolenglish.com/" + word + "/"
    print("working school url...:" + word + "   :: " + url)
    driver_get(url, driver)
    try:
        img_url = driver.find_elements_by_xpath("//meta[@property=\"og:image\"]")[0].get_property('content')
        print("working school image url..:" + img_url)
        raw_img = requests.get(img_url, headers=hdr).content
        img_path = image_temp_dir + word + "\\" + "working_school_" + word + get_img_type(img_url)
        print("working school image path..:" + img_path)
        write_raw_ing_file(raw_img, img_path)

    except Exception as e:
        print("Couldn't download image from working school for ..:" + word)
        print(e)


def scrap_phocabulary(word, driver, hdr):
    url = "http://phocabulary.com/word/" + word
    print("phocabulary url ...:" + word + "   :: " + url)
    driver_get(url, driver)
    # all_elem = driver.find_element_by_xpath("//*")
    # print(all_elem.get_attribute("outerHTML"))
    try:
        xpath = "//figure//img"
        img_url = driver.find_elements_by_xpath(xpath)
        count = 1
        for img in img_url:
            img_url = img.get_attribute('src')
            if "Blank" in img_url:
                continue
            print("phocabulary image url " + str(count) + " ...:" + str(img_url))
            raw_img = requests.get(img_url, headers=hdr).content
            img_path = image_temp_dir + word + "\\" + "phocabulary_" + word + str(count) + get_img_type(img_url)
            print("phocabulary image path..:" + img_path)
            write_raw_ing_file(raw_img, img_path)
            count = count + 1

    except Exception as e:
        print("Couldn't download image from phocabulary for ..:" + word)
        print(e)


def google_urls_scrap(word, driver):

    img_url_set = set([])

    define_word = "meaning+" + word
    url = "https://www.google.co.in/search?q=" + define_word + "&source=lnms&tbm=isch"
    # print(word + " :: " + url)
    driver_get(url, driver)
    img_div = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    for img in img_div:
        img_url = json.loads(img.get_attribute("innerHTML"))["ou"]
        if img_url not in img_url_set:
            img_url_set.add(img_url)

    # print("first fetch size of set..:" + str(len(img_url_set)))

    define_word = word + "+meaning"
    url = "https://www.google.co.in/search?q=" + define_word + "&source=lnms&tbm=isch"
    # print(word + " :: " + url)
    driver_get(url, driver)
    img_div = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    for img in img_div:
        img_url = json.loads(img.get_attribute("innerHTML"))["ou"]
        if img_url not in img_url_set:
            img_url_set.add(img_url)
    # print("word meaning fetch size of set..:" + str(len(img_url_set)))

    define_word = "define%3A+" + word
    url = "https://www.google.co.in/search?q=" + define_word + "&source=lnms&tbm=isch"
    # print(word + " :: " + url)
    driver_get(url, driver)
    img_div = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    for img in img_div:
        img_url = json.loads(img.get_attribute("innerHTML"))["ou"]
        if img_url not in img_url_set:
            img_url_set.add(img_url)
    # print("define fetch size of set..:" + str(len(img_url_set)))

    define_word = word + "+word+images"
    url = "https://www.google.co.in/search?q=" + define_word + "&source=lnms&tbm=isch"
    # print(word + " :: " + url)
    driver_get(url, driver)
    img_div = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    for img in img_div:
        img_url = json.loads(img.get_attribute("innerHTML"))["ou"]
        if img_url not in img_url_set:
            img_url_set.add(img_url)
    # print("word images fetch size of set..:" + str(len(img_url_set)))

    return img_url_set


def intelli_g(img_utl_set):
    '''trusted_urls = {'vocabmantra.com',
                    'slideplayer.com',
                    'thesaurus.plus',
                    'slideplayer.com',
                    'marketbusinessnews.com',
                    'easyangrezi.wordpress.com'
                    'bragitoff.com'
                    'quoracdn.net'
                    'study.com'
                    'weebly.com'
                    'aiyou.me'
                    }'''

    trusted_urls = {'vocabmantra.com',
                    'marketbusinessnews.com',
                    'easyangrezi.wordpress.com',
                    'bragitoff.com',
                    'study.com',
                    'weebly.com',
                    'aiyou.me',
                    'onlinegrecoaching.com',
                    'http://dani356.blogspot.com',
                    'wrbh.org',
                    'yourdictionary.com',
                    'reddit.com',
                    'quotemaster.org',
                    'studentnewsdaily.com',
                    'thefreedictionary.com',
                    'wikipedia.org',
                    'http://blog.writeathome.com',
                    'illustratedthesaurus.com',
                    'english.wifistudy.com',
                    'slideplayer.com',
                    'wikihow.com',
                    'wordsinasentence.com',
                    'livelaw.in',
                    'aminoapps.com',
                    'wordpress.com',
                    'zalarieunique.ru',
                    'http://hpssociety.info',

                    }
    high_trusted_urls = {'getwords.com', 'wordpandit.com', 'spinfold.com', 'dailyvocab.com'}

    final_urls = set([])
    for url in img_utl_set:
        for trust in trusted_urls:
            if trust in url:
                final_urls.add(url)
        '''for high_trust in high_trusted_urls:
            if high_trust in url:
                final_urls.add(url)'''

    return final_urls


def get_img_type(url):

    img_type = ""
    if '.jpg' in url:
        img_type = ".jpg"
    if '.png' in url:
        img_type = ".png"
    if '.gif' in url:
        img_type = ".gif"
    if '.jpeg' in url:
        img_type = ".jpeg"
    if img_type == "":
        img_type = ".jpg"

    return img_type


def scrap_common_images():

    words_list = open("D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json", "r")
    words_list_dict = json.load(words_list)["words"]
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://cssspritegenerator.com',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
    driver = webdriver.Firefox(executable_path='D:\drivers\win64\geckodriver.exe')
    hdr['User-Agent'] = get_random_user_agent()

    # shutil.rmtree(image_temp_dir)
    # os.mkdir(image_temp_dir)

    print("Launching firefox..")
    # logic is to download at least 5 (max 9) images from given 6 site.. if not then get from google using trusted sites
    for obj in words_list_dict:
        word = obj["WORD"].lower()
        word_dir = image_temp_dir + word

        if not os.path.exists(word_dir):
            os.mkdir(word_dir)
        elif os.listdir(word_dir):
            continue

        print(">>>>>>>>>>>>>>>  scrapping images for..: " + word + "....:   ")
        scrap_daily_vocab_img(word, driver, hdr)
        scrap_spin_fold_img(word, driver, hdr)
        scrap_get_word_img(word, driver, hdr)
        scrap_working_school(word, driver, hdr)
        scrap_phocabulary(word, driver, hdr)
        scrap_word_pandit_img(word, driver, hdr)

        if len(os.listdir(word_dir)) < 5:
            # need more images from google.. total images to download = 8
            img_count = 8 - (len(os.listdir(word_dir)))
            scrap_google_images(word, driver, hdr, img_count)

    driver.quit()
    words_list.close()
