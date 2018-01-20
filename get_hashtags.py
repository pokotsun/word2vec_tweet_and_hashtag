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

    params = {'count' : 100} # 取得数
    res = twitter.get(url, params = params)
    if res.status_code == 200:
        # 初期化
        hash_tags = []
        tweets = json.loads(res.text)['statuses']
        for i, tweet in enumerate(tweets):
            if i == 0:
                continue
            else:
                count+=1
                print(f'\n********{count}番目のtweet****************')
                print(f"tweet_id={tweet['id']}\n")
                print(f"created_at:{tweet['created_at']}\n")
                # tweetの本文をtextsに追加

                # ハッシュタグも追加していく
                hash_tags_tmp = tweet['entities']['hashtags']
                for hash_tag in hash_tags_tmp:
                    hash_tags.append(hash_tag['text'])

                max_id = tweet['id']
                print(f"hashtags={hash_tags}")
                _append_hashtags_to_file("hashtags_syokutyudoku2.txt", hash_tags)
                print('***************************************\n')
                # 各ファイルに追記していく


    elif(res.status_code == 429):
        print("Rate limitに引っかかったので15分休みます\n")
        sleep(910)
        print("15分休み終わりました\n")

    else: # 正常通信できなかった場合
        print(f"Failed: {res.status_code}")
        print(f"{res.text}")

def _append_hashtags_to_file(file_name, hashtags):
    with open(file_name, "a") as f:
        hash_words = ""
        print(f"hashtags in append: {hashtags}")
        for hashtag in hashtags:
            hash_words += f"{hashtag},"
        hash_words = hash_words[:-1]
        print(f"hash_words = {hash_words}\n")
        f.write(f"{hash_words}\n")
        f.close()

if __name__ == '__main__':
    main()
