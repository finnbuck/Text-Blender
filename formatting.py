with open("verbs.txt", "r", encoding="utf-8") as f:
    text = f.readlines()
    print(text[:10])
    text = [x.lower() for x in text if x != '\n']
    print(text[:10])
    string = ""
    for line in text:
        string += line
    print(string)


with open("new_verbs.txt", "w", encoding="utf-8") as f:
    
    f.write(string)






