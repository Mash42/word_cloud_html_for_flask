from flask import Flask, render_template, request, session
import pymysql
import requests
import re
from flask import Markup
import MeCab
import collections
import random
import os
#ワードクラウド
from wordcloud import WordCloud, ImageColorGenerator
#fpath = "C:\Windows\Fonts\meiryob.ttc" # fontは任意で
app = Flask(__name__)
app.secret_key = os.urandom(16)
def get_wordcrowd( text ):
    wordcloud = WordCloud(background_color="white",
                          width=800,
                          height=600,
                          #font_path=fpath,
                          collocations=False, # 単語の重複しないように
                         ).generate( text )
    wordcloud.to_file("wordcloud.png")
    wordcloud_svg = wordcloud.to_svg()
    f = open("/src/static/word_cloud/word_cloud.svg","w+")
    f.write(wordcloud_svg )
    f.close()
    #svg_document = svgwrite.Drawing(filename = "test-svgwrite.svg",profile = 'full')
    #svg_document.add(svg_document.text(wordcloud,
    #                                        insert = (210, 110)))
    #svg_document.tostring()
    #svg_document.save()

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
    return render_template("index.html")

# ホーム
@app.route('/create_word_cloud', methods=["GET", "POST"])
def create_word_cloud():
    SESSION_KEY_WORD_LIST = 'word_list'
    input_sentence = ""
    if SESSION_KEY_WORD_LIST in session:
        word_list = session[SESSION_KEY_WORD_LIST]
    if request.method == "POST":
        input_sentence = request.form["input_sentence"]
        word_list = list()
        #特定の品詞の単語を抽出
        mecab = MeCab.Tagger("-o chasen")
        mecab.parse('')
        node = mecab.parseToNode(input_sentence)
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
        word_counter = collections.Counter(words)
        for key in word_counter.keys():
            word_list.append({"word":key
                             ,"count":str(word_counter[key])
                             ,"size":str(word_counter[key]*len(word_list)/5)
                             ,"color":color_list[random.randrange(len(color_list))]
                             })

        session[SESSION_KEY_WORD_LIST] = word_list

        # ファイル作成
        get_wordcrowd(input_sentence)
    return render_template("index.html"
                          ,word_list=word_list
                          ,input_sentence=input_sentence
                          )

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

# アプリ起動
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
