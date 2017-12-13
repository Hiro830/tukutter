from datetime import  datetime
import MySQLdb
from flask import Flask, render_template,request,redirect,make_response

application = Flask(__name__)

@application.route('/')
def index1():
    return render_template('login.html')
@application.route('/login')
def index2():
    return render_template('login.html')

#@application.route('/plofile/<username>')
#def plofile(username=None):

@application.route('/follow/<username>')
def follow(username=None):
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()
      sql = 'SELECT * FROM users WHERE name = %s'
      con.execute(sql,[data])
      userinfo =con.fetchone()  #user_idを取得

      sql = 'SELECT * FROM follow WHERE follow_me = %s'
      con.execute(sql,[userinfo[0]])
      follow = con.fetchall()
      print(follow)
      if follow is ():   #値がないときって()でいいのか？？
        html = redirect('http://localhost:8080/top')
        sql = 'insert into follow(follow_me,follow_you) value (%s,%s)'
        con.execute(sql,[userinfo[0],username])
        db.commit()
      else:
        for row in follow:
            if row[2] == username:
              hantei = 10
              #delete
              ##sql = 'DELETE FROM follow WHERE id = %s'
              ##con.execute(sql,[row[0]])
              print(hantei)
            else:
              #insert
              ##sql = 'insert into follow(follow_me,follow_you) value (%s,%s)'
              ##con.execute(sql,[userinfo[0],username])
              ##db.commit()
              hantei = 20
              print(hantei)

      print(username)

      db.close()
      con.close()
      html = redirect('http://localhost:8080/top')

    return html


@application.route('/top')
def index3():
    #requestオブジェクトからCookieを取得する
    data = request.cookies.get('username', None)
    if data is None:    #cookieにuser情報がないときの処理 ログイン画面に飛ばす
      html = render_template('login.html')
    else:   #cookieにuser情報があるときの処理　表示する
      list=[]   #ツイートを格納する配列
      #mysqlに接続する
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()
      ######user情報全部引っ張ったほうがいいかも、user名とlogin名は違う#####
      sql = 'SELECT id FROM users WHERE name = %s'
      con.execute(sql,[data])
      userinfo =con.fetchone()  #user_idを取得

      sql = 'SELECT follow_you FROM follow WHERE follow_me = %s'
      con.execute(sql,[userinfo[0]])
      result = con.fetchall()
      test2 = result    #userがフォローしている人達のid

      for row in test2: #フォローしている人のツイートを取得
          sql = 'SELECT * from users inner join tweetInfo on tweetInfo.users_id = users.id WHERE users_id = %s'# order by tweetInfo.id desc
          ####↓にあるみたいに、left join加えてお気に入りがある場合は追加してなければNullを返す　値があれば色付きのがでるようにすればいい
          ####↓お気に入りかどうかは色で変更したいがそれはhtmlで実装するのかな？　ここからは値を渡して
          #SELECT * from (users inner join tweetInfo on tweetInfo.users_id = users.id) left join favorite on tweetInfo.id = favorite.tweet_id
          #print(row[0])
          con.execute(sql,[row[0]]) #各ユーザのツイート
          test3 = con.fetchall()
          for row in test3: #ツイート情報を個別に配列する
              list.append(row)
      html = render_template('index.html', id=userinfo[0],name=data,rows=list)
      #DBの切断
      db.close()
      con.close()
    return html

@application.route('/favoritelog')
def favarite_suru():
    #########tweetInfo.idが欲しい###########
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()

      sql = 'SELECT * FROM users WHERE name = %s'
      con.execute(sql,[data])
      userinfo =con.fetchone()  #user_idを取得


      db.close()
      con.close()

    return data

@application.route('/favorite')
def favarite():
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()
      ######user情報全部引っ張ったほうがいいかも、user名とlogin名は違う#####
      sql = 'SELECT * FROM users WHERE name = %s'
      con.execute(sql,[data])
      userinfo =con.fetchone()  #user_idを取得
      #print (userinfo)

      sql = 'select * from favorite where user_id = %s'
      con.execute(sql,[userinfo[0]])
      favarite_info = con.fetchall()
      print(favarite_info)
      if favarite_info is ():   #値がないときって()でいいのか？？
        html = redirect('http://localhost:8080/top')
      else:
        list=[]   #お気に入りのツイートを格納する配列
        for row in favarite_info: #favariteのtweetを1つずつ処理する
            print(row)
            sql = 'select * from tweetInfo where id = %s'
            sql = 'SELECT * from users inner join tweetInfo on tweetInfo.users_id = users.id WHERE tweetInfo.id = %s'
            con.execute(sql,[row[2]])
            tweet_info = con.fetchall()
            print(tweet_info)
            list.append(tweet_info[0])
            print(list[0][2]) #users_name
            print(list[0][9]) #tweet
            print(list[0][10])    #tweet_time
            #html = render_template('index.html', user=userinfo,favarites=list)
            html = render_template('index.html', id=userinfo[0],name=data,rows=list)
      #DBの切断
      db.close()
      con.close()
      print(data)
      #print (list)
      #print (list[1][2])

    return html

@application.route('/plofile/<username>')
def plofile(username=None):
    data = request.cookies.get('username', None)
    if data is None:    #cookieにuser情報がないときの処理 ログイン画面に飛ばす
      html = render_template('login.html')
    else:   #cookieにuser情報があるときの処理　表示する
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()

      sql = 'SELECT * FROM users WHERE name = %s'
      con.execute(sql,[data])
      user=con.fetchone()

      ##user情報を取得
      sql = 'SELECT * FROM users WHERE name = %s'
      con.execute(sql,[username])
      userinfo =con.fetchone()
      print (userinfo)
      if data == userinfo[2]:
        hantei = 1
      else:
        hantei = 0
      #user自身のツイートを取得
      #sql = 'select * from tweetInfo where users_id = %s'
      sql = 'SELECT * from users inner join tweetInfo on tweetInfo.users_id = users.id WHERE users_id = %s'
      con.execute(sql,[userinfo[0]])
      tweet_info = con.fetchall()
      print(tweet_info)
      tweet_list=[]
      for row in tweet_info:
          tweet_list.append(row)
      print(tweet_list)
      print(tweet_list[0][2])   #name
      print(tweet_list[0][9])   #tweet
      print(tweet_list[0][10])  #tweet_time
      print (hantei)

      db.close()
      con.close()
      html = render_template('profile.html', user=user,tweets=tweet_list,hantei = hantei)
    print(data)
    print(userinfo[2])
    print (hantei)
    return html

@application.route('/logout')
def logout_suru():
    html = make_response(render_template('login.html'))
    expires = 0
    Value = 'None'
    html.set_cookie('username', Value,expires)
    return html



@application.route('/search')
def search():
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()
      sql = 'SELECT * from users inner join tweetInfo on tweetInfo.users_id = users.id'
      con.execute(sql)
      tweet_info = con.fetchall()
      list=[]
      for row in tweet_info:
          list.append(row)

      db.close()  #DBの切断
      con.close()
      html = render_template('search.html',name=data,rows=list)
    return html

@application.route('/searchget',methods=['get'])
def search_get():
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()
      serch_word = request.args.get('search_query')
      print (serch_word)
      sql = 'SELECT * from tweetInfo where tweet like %s'
      con.execute(sql,[serch_word])
      tweet_info = con.fetchall()
      print(tweet_info)

      db.close()  #DBの切断
      con.close()
      html = render_template('search.html')
    return html

@application.route('/profile')
def profile_edit():
    return render_template('profile_edit.html')

@application.route('/profile', methods=['POST'])
def profile_write():
    pic = request.form['file']
    userid = request.form['login_ID']
    n_pass = request.form['Pass']       #password
    re_pass = request.form['Re_Pass']
    name = request.form['username']       #username
    intro = request.form['intro']

    print(pic)
    print(userid)
    print(n_pass)
    print(re_pass)
    print(name)
    print(intro)
    return intro

@application.route('/new')
def show_new():
    #新規追加画面を表示する
    html = render_template('registration.html')
    return html

@application.route('/new', methods=['POST'])
def donew():

    login_n = request.form['new_login_ID']  #login_id
    pass_n = request.form['new_Pass']       #password
    re_pass_n = request.form['new_Re_Pass']
    name_n = request.form['new_name']       #username

#####入力がなかった場合はもう一度入力してくださいってでるようにしたい#####
    if pass_n == re_pass_n:  #照合に合格した時の処理
      #mysqlに接続する
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()
      #取得したタスクの内容をtodoテーブルに追加する
      sql = 'insert into users(Login,name,pass) value (%s,%s,%s)'
      con.execute(sql,[login_n,name_n,pass_n])
      db.commit()
      #DBの切断
      db.close()
      con.close()

      html = render_template('login.html')
    else:
      pass  #処理をかかないとエラーになる
      ##照合に失敗したときの処理後で書く
    return html

@application.route('/tubuyaita-')
def tubuyaki1():
    #新規追加画面を表示する
    return render_template('tweet.html')

@application.route('/tubuyaita-', methods=['POST'])
def tubuyaki2():
    tubuyaki = request.form['tweet']  #login_id
    #mysqlに接続する
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()

    data = request.cookies.get('username', None)    #cookieからuser名を取得

    sql = 'SELECT id FROM users WHERE name = %s'
    con.execute(sql,[data])
    userinfo =con.fetchone()

    sql = 'insert into tweetInfo(users_id,tweet) value (%s,%s)' #time_nowも追加必要
    con.execute(sql,[userinfo[0],tubuyaki])
    db.commit()
    #DBの切断
    db.close()
    con.close()
    return redirect('http://localhost:8080/top')

@application.route('/login', methods=['POST'])
def login_suru():
    login_G = request.form['login_ID']
    Pass_G = request.form['Password']

    #mysqlに接続する
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()

    #user情報を取得する
    sql = 'SELECT * FROM users WHERE Login = %s'
    con.execute(sql,[login_G])
    userinfo = con.fetchall()
    test_id = userinfo[0][0]    #id
    test_name = userinfo[0][2]  #name
    test_pass = userinfo[0][3]  #pass

    #passの照合を行う
    if userinfo[0][3] == Pass_G:  #照合に合格した時の処理
      #html = make_response(render_template('index.html', id=test_id,name=test_name,rows=list))
      html = make_response(redirect('http://localhost:8080/top'))
      max_age = 60 * 60 * 24 * 120 # 120 days
      expires = int(datetime.now().timestamp()) #+ max_age
      html.set_cookie('username', test_name,expires)    #cookieをset users_name

    else:   #照合に失敗した場合の処理を記入する
      html = render_template('login.html')

    #DBの切断
    db.close()
    con.close()

    return html
