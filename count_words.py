
from country import countries
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
import nltk

nltk.download('stopwords')

tokenizer = RegexpTokenizer(r'[a-zA-Z]\w+\'?\w*')
stop_words = set(stopwords.words('english'))

pos_neg_words = {}
sentiment_results = {}


def get_pos_neg_words():
    pos_file = open('pos.txt', 'r', encoding="utf-8",
                    errors="ignore").readlines()
    pos = []
    for i in pos_file:
        pos += tokenizer.tokenize(i)

    for w in pos:
        pos_neg_words[w] = 'positive'

    neg_file = open('neg.txt', 'r', encoding="utf-8",
                    errors="ignore").readlines()
    neg = []
    for i in neg_file:
        neg += tokenizer.tokenize(i)

    for w1 in neg:
        pos_neg_words[w1] = 'negative'


get_pos_neg_words()


def get_word_counts():
    for country in countries:
        if country == "Malaysia - Kuala Lumpur (KUL)":
            continue
        text = open("news_feed/" + country + ".txt",
                    encoding="utf-8", errors="ignore").readlines()
        result = {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'positive_pct': 0,
            'negative_pct': 0,
            'neutral_pct': 0,
            'sentiment': 0,
            'stop_words': 0,
            'words': {}
        }
        # data format for result:
        # result = {
        #     "country A": {
        #         'positive': 0,
        #         'negative': 0,
        #         'neutral': 0,
        #         'positive_pct': 0,
        #         'negative_pct': 0,
        #         'neutral_pct': 0,
        #         'sentiment': 0,
        #         'words': {
        #             "A": 1,
        #             "B": 2,
        #         }
        #     }
        # }
        for i in text:
            word = tokenizer.tokenize(i)
            for w in word:
                w_base = w.lower()
                if w_base in stop_words:
                    result["stop_words"] += 1
                    continue
                if len(w_base) <= 2:
                    continue
                # word count
                if w_base in result["words"]:
                    result["words"][w_base] += 1
                else:
                    result["words"][w_base] = 1
                # sentiment analysis
                if w_base in pos_neg_words:
                    result[pos_neg_words[w_base]] += 1
                else:
                    result["neutral"] += 1
            # calculate percentage
            total_words = result["positive"] + \
                result["negative"] + result["neutral"]
            result["positive_pct"] = round(
                (result["positive"]/total_words) * 100, 2)
            result["negative_pct"] = round(
                (result["negative"]/total_words) * 100, 2)
            result["neutral_pct"] = round(
                (result["neutral"]/total_words) * 100, 2)
            if result["positive"] != 0 and result["negative"] != 0:
                result["sentiment"] = round((result["positive"] -
                                             result["negative"]) / (result["positive"] + result["negative"]) * 100, 2)
        sentiment_results[country] = result


get_word_counts()


# Removed rabin karp
def rabin_karp(pat, txt, q, d=256):
    global sentiment_results
    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0  # hash value for pattern
    t = 0  # hash value for txt
    h = 1

    # The value of h would be "pow(d, M-1)%q"
    for i in range(M - 1):
        h = (h * d) % q

        # Calculate the hash value of pattern and first window
    # of text
    for i in range(M):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q

        # Slide the pattern over text one by one
    for i in range(N - M + 1):
        # Check the hash values of current window of text and
        # pattern if the hash values match then only check
        # for characters on by one
        if p == t:
            # Check for characters one by one
            for j in range(M):
                if txt[i + j] != pat[j]:
                    break

            j += 1
            # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
            if j == M:
                return True

                # Calculate hash value for next window of text: Remove
        # leading digit, add trailing digit
        if i < N - M:
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q

            # We might get negative values of t, converting it to
            # positive
            if t < 0:
                t = t + q
    return False


def rk_delete_word(country_text):
    global sentiment_results
    global stop_words
    for result in sentiment_results:
        text = result["words"]
        new_text = text
        for t in text:
            flag = False
            for pat in stop_words:
                flag = rabin_karp(pat, text, 101)
                if flag:
                    break
            if flag:
                new_text.pop(t, None)
        result["words"] = new_text


if __name__ == '__main__':
    outfile = open('test.txt', 'w')
    print(sentiment_results, file=outfile)
