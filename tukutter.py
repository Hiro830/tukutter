import MySQLdb
from flask import Flask, render_template,request,redirect

application = Flask(__name__)
@application.route('/')
def index():
    return redirect('http://localhost:8080/static/login.html')

@application.route('/login', methods=['POST'])
def login_suru():
    login_G = request.form['login_ID']
    Pass_G = request.form['Password']
    #mysqlに接続する
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter', charset='utf8')
    con = db.cursor()

    #user情報を取得する
    sql = 'SELECT * FROM users WHERE Login = %s'
    con.execute(sql,[login_G])
    userinfo = con.fetchall()
    #print (userinfo)
    #print (userinfo[0][0])
    test_id = userinfo[0][0]    #id
    test_name = userinfo[0][2]  #name
    test_pass = userinfo[0][3]  #pass

    #passの照合を行う
    if userinfo[0][3] == Pass_G:  #照合に合格した時の処理
      list=[]   #ツイートを格納する配列
      #sql = 'SELECT tweet,delete_flg FROM tweetInfo WHERE users_id = %s'
      sql = 'SELECT * from users inner join tweetInfo on tweetInfo.users_id = users.id WHERE users_id = %s'
      con.execute(sql,[test_id])
      test1 = con.fetchall()    #userのツイート
      for row in test1:     #ツイート情報を個別に配列する
          list.append(row)  #userのツイートを格納する

        ##userのフォローしている人のツイート情報を検索する##
      sql = 'SELECT follow_you FROM follow WHERE follow_me = %s'
      con.execute(sql,[test_id])
      result = con.fetchall()
      test2 = result    #userがフォローしている人達のid

      for row in test2: #フォローしている人のツイートを取得
          #sql = 'SELECT tweet,delete_flg FROM tweetInfo WHERE users_id = %s'
          sql = 'SELECT * from users inner join tweetInfo on tweetInfo.users_id = users.id WHERE users_id = %s'
          #print(row[0])
          con.execute(sql,[row[0]]) #各ユーザのツイート
          test3 = con.fetchall()    #各ユーザのツイート
          for row in test3: #ツイート情報を個別に配列する
              print (row[0])    #users_id
              print(row[2])     #users_name
              print(row[5])     #tweet_id
              print(row[7])     #tweet
              print(row[8])     #tweet_time

              list.append(row)

##topに反映できるようにhtmlも変更必要##
      html = render_template('top.html', name=test_name,row=list)

    else:   #照合に失敗した場合の処理を記入する
      print('間違ってます')

    print (list)
    #print(list[0][1])

    #DBの切断
    db.close()
    con.close()
    return html
