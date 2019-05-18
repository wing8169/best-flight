from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

tokenizer = RegexpTokenizer(r'[a-zA-Z]\w+\'?\w*')

def get_countries():
    text = open('map.txt', 'r')
    content = text.read()
    text.close()
    return content.strip().split("\n")

countries = get_countries()

#=============================================
def get_word_type():
    pos_ng_words = {} 
    
    pos_file = open('news_feed\\pos.txt', 'r').readlines()
    pos = []
    for i in pos_file:
        pos += tokenizer.tokenize(i)
    
    for w in pos:
        pos_ng_words[w] = 'positive'
    
    #================================
    neg_file = open('news_feed\\neg.txt', 'r').readlines()
    neg = []
    for i in neg_file:
        neg += tokenizer.tokenize(i) 

    for w1 in neg:
        pos_ng_words[w1] = 'negative'

    return pos_ng_words

word_type = get_word_type()

