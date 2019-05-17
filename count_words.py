
from nltk.stem import PorterStemmer
from country import countries

from nltk.corpus import stopwords
import string
import nltk
nltk.download('stopwords')

pm = PorterStemmer()
translator = str.maketrans('', '', string.punctuation)
stop_words = set(stopwords.words('english'))
word_counts = {}


def get_word_counts():
    for country in countries:
        if country == "Malaysia - Kuala Lumpur (KUL)":
            continue
        hand = open("news_feed/" + country + ".txt",
                    encoding="utf-8", errors="ignore")
        di = dict()
        for i in hand:
            word = i.lower().rstrip().split()
            for w in word:
                w_base = pm.stem(w.translate(translator))
                if w_base in stop_words or len(w_base) <= 2:
                    continue
                if w_base in di:
                    di[w_base] += 1
                else:
                    di[w_base] = 1
        word_counts[country] = di


get_word_counts()

if __name__ == '__main__':
    outfile = open('test.txt', 'w')
    print(word_counts, file=outfile)
