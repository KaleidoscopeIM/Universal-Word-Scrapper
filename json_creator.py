import json
from gre_words_scripts.utils import clean_data_from_html


def json_creator_barrons():

    print("creating barron 333 and 800 ..:")
    filein = open("D:\Video Work Area\GRE WORDS APP\data\production\WordsList.json", "r")
    filein_obj = json.load(filein)["words"]

    barron800_words_in = open("D:\Video Work Area\GRE WORDS APP\data\Barron800WordsList.txt", "r")
    barron800_json_out = open("D:\Video Work Area\GRE WORDS APP\data\production\Barron800.json", "w")
    barron800_json_out.seek(0)
    barron800_json_out.truncate()

    barron333_words_in = open("D:\Video Work Area\GRE WORDS APP\data\Barron333WordsList.txt", "r")
    barron333_json_out = open("D:\Video Work Area\GRE WORDS APP\data\production\Barron333.json", "w")
    barron333_json_out.seek(0)
    barron333_json_out.truncate()

    barron800_final_string = "{\"BARRON800\":["
    barron333_final_string = "{\"BARRON333\":["

    for obj in filein_obj:
        word = clean_data_from_html(obj["WORD"])
        barron800_words_in.seek(0)
        barron333_words_in.seek(0)
        wid = obj["ID"]
        for barron800_word in barron800_words_in:
            if word == clean_data_from_html(barron800_word):
                barron800_final_string = barron800_final_string + "{\"BARRONID\":" + str(wid) + "},"
                break
        for barron333_word in barron333_words_in:
            if word == clean_data_from_html(barron333_word):
                barron333_final_string = barron333_final_string + "{\"BARRONID\":" + str(wid) + "},"
                break

    barron333_final_string = barron333_final_string[:-1]
    barron800_final_string = barron800_final_string[:-1]

    barron333_final_string = barron333_final_string + "]}"
    barron800_final_string = barron800_final_string + "]}"

    print("generated barron 333 string..:"+barron333_final_string)
    print("generated barron 800 string..:" + barron800_final_string)

    barron333_json_out.write(barron333_final_string)
    barron800_json_out.write(barron800_final_string)
    barron333_json_out.flush()
    barron800_json_out.flush()

    barron800_json_out.close()
    barron333_json_out.close()
    barron800_words_in.close()
    barron333_words_in.close()
