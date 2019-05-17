from nltk.corpus import stopwords
import string
import nltk
nltk.download('stopwords')


with open('Bangkok.txt', 'r') as inFile, open('BangkokNew.txt', 'w') as outFile:
    for line in inFile.readlines():
        print(" ".join([word for word in line.lower().translate(str.maketrans('', '', string.punctuation)).split()
                        if len(word) >= 4 and word not in stopwords.words('english')]), file=outFile)


with open('Beijing.txt', 'r') as inFile, open('BeijingNew.txt', 'w') as outFile:
    for line in inFile.readlines():
        print(" ".join([word for word in line.lower().translate(str.maketrans('', '', string.punctuation)).split()
                        if len(word) >= 4 and word not in stopwords.words('english')]), file=outFile)


with open('Brunei.txt', 'r') as inFile, open('BruneiNew.txt', 'w') as outFile:
    for line in inFile.readlines():
        print(" ".join([word for word in line.lower().translate(str.maketrans('', '', string.punctuation)).split()
                        if len(word) >= 4 and word not in stopwords.words('english')]), file=outFile)


with open('Indonesia.txt', 'r') as inFile, open('IndonesiaNew.txt', 'w') as outFile:
    for line in inFile.readlines():
        print(" ".join([word for word in line.lower().translate(str.maketrans('', '', string.punctuation)).split()
                        if len(word) >= 4 and word not in stopwords.words('english')]), file=outFile)


with open('Melbourne.txt', 'r') as inFile, open('MelbourneNew.txt', 'w') as outFile:
    for line in inFile.readlines():
        print(" ".join([word for word in line.lower().translate(str.maketrans('', '', string.punctuation)).split()
                        if len(word) >= 4 and word not in stopwords.words('english')]), file=outFile)


with open('Tokyo.txt', 'r') as inFile, open('TokyoNew.txt', 'w') as outFile:
    for line in inFile.readlines():
        print(" ".join([word for word in line.lower().translate(str.maketrans('', '', string.punctuation)).split()
                        if len(word) >= 4 and word not in stopwords.words('english')]), file=outFile)
