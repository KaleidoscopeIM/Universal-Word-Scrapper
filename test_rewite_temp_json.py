from pyquery import PyQuery
from bs4 import BeautifulSoup
'''
file = open(r"D:\Video Work Area\GRE WORDS APP\data\test\all.html", 'r').read()
fout = open(r"D:\Video Work Area\GRE WORDS APP\data\Barron1100WordsList.txt", 'w')
fin = open(r"D:\Video Work Area\GRE WORDS APP\data\test\fin.txt", 'r')
fidioms = open(r"D:\Video Work Area\GRE WORDS APP\data\Barron1100Idioms.txt", 'w')

filesoup = BeautifulSoup(file, features="html.parser")
words = filesoup.find_all("tr")


skip = False
count = 0
idioms = 0
for line in fin:
    line = line.capitalize()
    if line == "" or line == "\n" or skip:
        skip = False
        continue
    print(line)
    count = count+1
    skip = True
    fout.write(line)
    if " " in line:
        print("idioms found..: "+line)
        fidioms.write(line)
        idioms = idioms + 1

print(count)
print(idioms)
fidioms.close()
fin.close()
fout.flush()
fout.close()'''

finalMerge = open(r"D:\Video Work Area\GRE WORDS APP\data\test\all_words.txt", 'w')
wordsin= open(r"D:\Video Work Area\GRE WORDS APP\data\all_words.txt", 'r')
b1100file = open(r"D:\Video Work Area\GRE WORDS APP\data\Barron1100WordsList.txt", 'r')
fromallwords = 0
from1100file = 0
words_set = set([])
for line in wordsin:
    words_set.add(line)
for line in b1100file:
    words_set.add(line)
new_set = sorted(words_set)
for word in new_set:
    finalMerge.write(word)

finalMerge.flush()
print(len(words_set))
'''for line in b1100file:
    found = False
    for aWord in wordsin:
        if line == aWord:
            found = True
            finalMerge.write(aWord)
            fromallwords = fromallwords + 1
            break
    wordsin.seek(0)
    if found is False:
        finalMerge.write(line)
        from1100file = from1100file + 1


print("from all words :" + str(fromallwords))
print("from all 1100 file :" + str(from1100file))'''
finalMerge.flush()
finalMerge.close()
wordsin.close()
b1100file.close()

'''

finalMerge = open(r"D:\Video Work Area\GRE WORDS APP\data\test\all_words.txt", 'r')
wordsin= open(r"D:\Video Work Area\GRE WORDS APP\data\all_words.txt", 'r')
for line in finalMerge:
    found = False
    for aWord in wordsin:
        if line == aWord:
            found = True
            break
    if found is False:
        print("not found :" + line)'''