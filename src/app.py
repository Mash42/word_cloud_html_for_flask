from flask import Flask, render_template, request
import pymysql
import requests
import re
from flask import Markup

app = Flask(__name__)

# データベースコネクション情報
MYSQL_OPTIONS = {"host": 'db'
                ,"port": 3306
                ,"user": 'hoge_user'
                ,"passwd": 'hoge_pass_db'
                ,"db": 'hoge_db'
                ,"charset": 'utf8'
                }

# ホーム
@app.route('/', methods=["GET", "POST"])
def index():
    # テストデータを作成する(本来はDBなどから取ってくる)
    word_list = list()
    word_list.append({ "word": "China", "size": "50", "color": "#A4CABC" })
    word_list.append({ "word": "India", "size": "40", "color": "#A4CABC" })
    word_list.append({ "word": "Indonesia", "size": "30", "color": "#A4CABC" })
    word_list.append({ "word": "Algeria", "size": "40", "color": "#EAB364" })
    word_list.append({ "word": "Congo", "size": "30", "color": "#EAB364" })
    word_list.append({ "word": "Sudan", "size": "20", "color": "#EAB364" })
    word_list.append({ "word": "Russia", "size": "60", "color": "#DDA288" })
    word_list.append({ "word": "Kazakhstan", "size": "50", "color": "#DDA288" })
    word_list.append({ "word": "Ukraine", "size": "40", "color": "#DDA288" })
    word_list.append({ "word": "Canada", "size": "50", "color": "#ACBD78" })
    word_list.append({ "word": "America", "size": "40", "color": "#ACBD78" })
    word_list.append({ "word": "Mexico", "size": "30", "color": "#ACBD78" })
    word_list.append({ "word": "Brazil", "size": "40", "color": "#A5C3CF" })
    word_list.append({ "word": "Columbia", "size": "30", "color": "#A5C3CF" })
    word_list.append({ "word": "Argentina", "size": "20", "color": "#A5C3CF" })
    return render_template("index.html"
                          ,word_list=word_list
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
