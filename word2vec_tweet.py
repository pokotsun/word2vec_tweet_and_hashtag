from utils import util
from gensim.models import word2vec
from gensim import corpora
import logging
import sys

def main():
    print("Hello, word2vec")
    # words = [['あ', 'い'], ['う', 'え']]
    # _make_dictionary("texts/tweets_syokutyudoku.txt", 'syokutyudoku_tweet_dictionary.txt')
    # dictionary = corpora.Dictionary.load_from_text('syokutyudoku_tweet_dictionary.txt')
    # words = util.get_tweet_words("texts/tweets_syokutyudoku.txt")
    _save_model(util.get_tweet_words("texts/tweets_syokutyudoku.txt"))

    show_answer()

# BOW用の辞書作成
def _make_dictionary(src_name, output_name):
    words = util.get_tweet_words(src_name)
    dictionary = corpora.Dictionary(words)
    print(f"dictionary: {dictionary}")
    dictionary.save_as_text(output_name)


# Word2Vec用のmodelを生成する
def _save_model(words):
    model = word2vec.Word2Vec(words, size=600, min_count=40, window=5)
    model.save("./syokutyudoku.model")



def show_answer():
    model = word2vec.Word2Vec.load("syokutyudoku.model")

    argvs = sys.argv
    if len(argvs) == 2:
        word = argvs[1]
        print(f"word[{word}]に近いワードは以下の単語たちです。")
        similar_words = model.wv.most_similar(word)
        print("(似ているワード , 類似度)")
        for v in similar_words:
            print(f"{v}")
    elif len(argvs) == 3:
        word1 = argvs[1]
        word2 = argvs[2]
        similarity = model.similarity(word1, word2)
        print(f"{word1}と{word2}の類似度は{similarity}です。\n")
    else:
        print("""単語を一つ入力した際は、入力ワードに近いものを上から10こ表示します。\n
        単語を２つ入力した際は、その入力ワード2つの類似度を表示します""")

if __name__ == '__main__':
    main()
