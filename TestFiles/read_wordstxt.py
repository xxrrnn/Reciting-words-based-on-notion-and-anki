with open("TxtDataFiles/words.txt","r",encoding="utf-8") as file:
    words = file.readlines()
for word in words:
    print(word)
print(words)