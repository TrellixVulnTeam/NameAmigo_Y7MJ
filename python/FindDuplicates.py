import ReadText as rt

words = rt.readText('../txt/words.txt')

d = {}
for i in range(len(words)):
    if words[i] in d.keys():
        print("DUP:", words[i])
    d.update({words[i]:1})

