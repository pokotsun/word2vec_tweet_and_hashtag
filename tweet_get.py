import json
from time import sleep
from config import config # 標準のjsonモジュールだとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session # OAuthのライブラリの読み込み

# グローバル変数を指定
max_id = 0
count = 0

# main関数
def main():

    CK = config.CONSUMER_KEY
    CS = config.CONSUMER_SECRET
    AT = config.ACCESS_TOKEN
    ATS = config.ACCESS_TOKEN_SECRET

    twitter = OAuth1Session(CK, CS, AT, ATS) # 認証処理
    # print(f'max_id = {max_id}')

    for i in range(0,50):
        get_tweets(twitter)
        print(f'max_id = {max_id}')

# print(f"res={res.text}")

def get_tweets(twitter):
    global max_id, count # グローバル宣言されているmax_idを使う

    url = config.TWEET_QUARY
    # print(f"{max_id}: {url}")

    if max_id != 0:
        url += f"&max_id={max_id}" # タイムライン取得エンドポイント

    params = {'count' : 100, 'filter' : 'retweet'} # 取得数
    res = twitter.get(url, params = params)
    if res.status_code == 200:
        # 初期化
        texts = []
        hash_tags = []

        tweets = json.loads(res.text)['statuses']
        for i, tweet in enumerate(tweets):
            if i == 0 and not first_flg:
                continue
            else:
                count+=1
                print(f'\n********{count}番目のtweet****************')
                print(f"tweet_id={tweet['id']}\n")
                print(f"created_at:{tweet['created_at']}\n")
                # tweetの本文をtextsに追加
                text = tweet['text']
                print(f"text = {text}")
                texts.append(text.replace("[", "").replace("]", "").replace("\'", "").replace("#", "").replace("\n", ""))

                # ハッシュタグも追加していく
                hash_tags_tmp = tweet['entities']['hashtags']
                for hash_tag in hash_tags_tmp:
                    print(f"hash_tag: {hash_tag['text']}")
                    hash_tags.append(hash_tag['text'])

                max_id = tweet['id']
                print('***************************************\n')
                # 各ファイルに追記していく
                _append_tweet_to_file("tweets_syokutyudoku.txt", texts)
                _append_hashtags_to_file("hashtags_syokutyudoku.txt", hash_tags)


    elif(res.status_code == 429):
        print("Rate limitに引っかかったので15分休みます\n")
        sleep(910)
        print("15分休み終わりました\n")

    else: # 正常通信できなかった場合
        print(f"Failed: {res.status_code}")
        print(f"{res.text}")

def _append_tweet_to_file(file_name, data):
    with open(file_name, "a") as f:
        f.write(f"{data}\n")
        f.close()

def _append_hashtags_to_file(file_name, hashtags):
    with open(file_name, "a") as f:
        hash_words = ""
        for hashtag in hashtags:
            hash_words += f"{hashtag},"
        # print(f"hash_words = {hash_words}\n")
        hash_words = hash_words[:-1]
        f.write(f"{hash_words}\n")
        f.close()

if __name__ == '__main__':
    main()
