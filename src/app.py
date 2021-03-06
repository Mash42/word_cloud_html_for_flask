from flask import Flask, render_template, request, session
import pymysql
import requests
import re
from flask import Markup
import MeCab
import collections
import random
import os
import datetime
#ワードクラウド
from wordcloud import WordCloud, ImageColorGenerator
app = Flask(__name__)
app.secret_key = os.urandom(16)

WORDCLOUD_FONT_PATH = "/src/static/wordcloud/font/Noto-hinted/NotoSansCJKjp-Regular.otf"
# データベースコネクション情報
MYSQL_OPTIONS = {"host": 'db'
                ,"port": 3306
                ,"user": 'hoge_user'
                ,"passwd": 'hoge_pass_db'
                ,"db": 'hoge_db'
                ,"charset": 'utf8'
                }
color_list = ["#A4CABC"
             ,"#EAB364"
             ,"#DDA288"
             ,"#ACBD78"
             ,"#A5C3CF"
             ]
# ホーム
@app.route('/', methods=["GET", "POST"])
def index():
    new_time = datetime.datetime.now().strftime('%H:%M:%S')
    return render_template("index.html"
                          ,new_time=new_time)

# ホーム
@app.route('/create_wordcloud', methods=["GET", "POST"])
def create_wordcloud():
    new_time = datetime.datetime.now().strftime('%H:%M:%S')
    file_name = ""
    input_sentence = ""
    wordcloud_width = None
    if request.method == "POST":
        input_sentence = request.form["input_sentence"]
        wordcloud_width = request.form["wordcloud_width"]
        words = get_words_for_mecab(input_sentence)
        #日本語だけに絞る
        japanane_words = list()
        for word in words:
            # ワードが英数字ではない場合
            if not isalnum(word) and len(word) > 1 and not "://" in word and not "_________" in word:
                japanane_words.append(word)
        # ファイル作成
        file_name = create_wordcrowd(" ".join(japanane_words)
                                    ,int(wordcloud_width)
                                    ,int(wordcloud_width)//2
                                    ,WORDCLOUD_FONT_PATH)
        # ワード出現回数のカウント
        word_count_dict = collections.Counter(japanane_words)
        word_count_list = list()
        for key in word_count_dict:
            word_count_list.append({"word":key
                                   ,"count":word_count_dict[key]
                                   })
        word_count_list = sorted(word_count_list, key=lambda x:x['count'], reverse=True)[:10]
        #print(word_count_list)
    return render_template("index.html"
                          ,input_sentence=input_sentence
                          ,file_name=file_name
                          ,wordcloud_width=wordcloud_width
                          ,new_time=new_time
                          ,word_count_list=word_count_list
                          )
# ワードクラウド作成
def create_wordcrowd(text, width, height, font_path):
    wordcloud = WordCloud(background_color="black"
                          ,width=width
                          ,height=height
                          ,collocations=False # 単語の重複しないように
                          ,font_path=font_path
                         ).generate( text )
    wordcloud_svg = wordcloud.to_svg()
    file_name = None
    f = open("/src/static/wordcloud/wordcloud.svg","w+", encoding="utf_8")
    file_name = f.name
    f.write(wordcloud_svg)
    f.close()

    return file_name

#入力された文章を単語分けして返却(MeCab使用)
def get_words_for_mecab(sentence):
    word_list = list()
    #特定の品詞の単語を抽出
    mecab = MeCab.Tagger("-o chasen")
    mecab.parse('')
    node = mecab.parseToNode(sentence)
    words = list()
    while node:
        if node.feature.split(",")[0] == "名詞":
            word = node.surface
            words.append(word)
            #print("名詞=>" + word)
        elif node.feature.split(",")[0] == "動詞":
            word = node.surface
            words.append(word)
            #print("動詞=>" + word)
        elif node.feature.split(",")[0] == "形容詞":
            word = node.surface
            words.append(word)
            #print("形容詞=>" + word)
        elif node.feature.split(",")[0] == "形容動詞":
            word = node.surface
            words.append(word)
            #print("形容動詞=>" + word)
        else:
            pass
        node = node.next
    return words
# データベースコネクション取得
def getConnection():
    conn = pymysql.connect(host=MYSQL_OPTIONS['host']
                          ,port=MYSQL_OPTIONS['port']
                          ,user=MYSQL_OPTIONS['user']
                          ,passwd=MYSQL_OPTIONS['passwd']
                          ,db=MYSQL_OPTIONS['db']
                          ,charset=MYSQL_OPTIONS['charset']
                          ,cursorclass=pymysql.cursors.DictCursor
                          )
    return conn
#半角英数字
alnumReg = re.compile(r'^[a-zA-Z0-9]+$')
def isalnum(s):
    return alnumReg.match(s) is not None
# アプリ起動
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
