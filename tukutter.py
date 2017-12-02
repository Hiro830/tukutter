import MySQLdb
from flask import Flask, render_template,request,redirect

application = Flask(__name__)

@application.route('/login', methods=['POST'])
def login_suru():
    login_G = request.form['login_ID']
    Pass_G = request.form['Password']
    #mysqlに接続する
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter', charset='utf8')
    con = db.cursor()

    #userのpassとidを取得する
    sql = 'SELECT pass FROM users WHERE Login = %s'
    con.execute(sql,[login_G])
    result = con.fetchall()
    #print (result)
    task = result[0][0]
    #print (task)
    sql1 = 'SELECT id FROM users WHERE Login = %s'
    con.execute(sql1,[login_G])
    result = con.fetchall()
    test=result[0][0]

    #passの照合を行う
    if task == Pass_G:  #照合に合格した時の処理
        ##userのフォローしている人のツイート情報を検索する##
      ##userがフォローしている人のidを検索する
      sql = 'SELECT follow_you FROM follow WHERE follow_me = %s'
      con.execute(sql,[test])
      result = con.fetchall()
      test1 = result
      #print(test1)

      ##uerがフォローしている複数の全部の人(test1)のツイート取得したい
      for row in test1: #test1自体が配列になってるからtest1[]にすると処理できない
          sql = 'SELECT tweet FROM tweetInfo WHERE users_id = %s'
          #print(row[0])
          con.execute(sql,[row[0]])
          result = con.fetchall()
          ###ツイートを一つの関数にまとめたい
          test2 = result
          print (test2)

##topに反映できるようにhtmlも変更必要##
      #html = render_template('top.html', name=test,***=test2)

    else:   #照合に失敗した場合の処理を記入する
      print('間違ってます')

    print (test2)

    #DBの切断
    db.close()
    con.close()

    #print(html)
    return task
    return redirect('http://localhost:8080/static/login.html')
