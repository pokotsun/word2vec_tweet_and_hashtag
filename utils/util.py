import sys
import MeCab
import re

input_poses = ['名詞', '形容詞', '動詞']

def get_tweet_words(file_path):
    tweet_word_list = []
    with open(file_path, 'r') as f:
        m = MeCab.Tagger ("-Ochasen")
        # ここで1ツイートのテキストが格納される
        for tweet in f:
            processed_tweet = _mojiretu_processing(tweet)
            keywords = m.parse(processed_tweet)
            tweet_word_list.append(_getWordsFromTweet(keywords))
            # print("/***************************/")

        # print(f"tweet_word_list:{tweet_word_list}")
        f.close()

    return tweet_word_list

    # print(tweet_list)

# 文字列の解析
def _mojiretu_processing(text):
    rtn = re.sub("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", text)
    rtn = re.sub(r"\\u[0-9]+", "", rtn)
    return rtn

# tweetから単語列を取り出す
# word_info[0] : など
# word_info[1] : ナド 読み
# word_info[2] : など 一般形
# word_info[3] : 助詞-助動詞 品詞
def _getWordsFromTweet(keywords):
    global input_poses
    words = []
    # print (f"Mecab解析結果{keywords}")
    # rowにはtweet内の1単語の各情報が入る
    for row in keywords.split("\n"):
        word_info = row.split("\t")
        # print(f"word_info: {word_info}")
        if word_info[0] == 'EOS': # EOSだったら終わる
            # print("エンドオブセンテンスです\n")
            break
        else:
            pos = word_info[3]
            stem = pos.split('-')[0]
            # print(f"pos = {pos}")
            # print(f"stem = {stem}")
            if stem in input_poses: # 取ってきたstemが取得すべきstemならば
                words.append(word_info[2])

    return words
