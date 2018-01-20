import sys
import re
def get_hashtag_words(file_path):
    hashtag_list = []
    with open(file_path, 'r') as f:
        for row in f:
            words = row.replace("\n", "")
            words = words.split(',')
            # print(f"words={words}\n")
            hashtag_list.append(words)

        f.close()
    return hashtag_list
#
# if __name__=="__main__":
#     get_hashtag_words("texts/hashtags_syokutyudoku.txt")
