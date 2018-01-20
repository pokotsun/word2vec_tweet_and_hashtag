# 取ってきた単語を頻度順に並べる
from collections import Counter
from utils import util

words = util.get_tweet_words("texts/tweets_syokutyudoku.txt")

words_list = []
iterator = (i for i in (row for row in words))
for i in iterator:
    words_list.extend(i)

counter = Counter(words_list)
with open('word_count.txt', 'w') as f:
    for word, cnt in counter.most_common():
        f.write(f"{word}: {cnt}\n")
    f.close()
