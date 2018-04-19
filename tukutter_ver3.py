from datetime import  datetime
import MySQLdb
from flask import Flask, render_template,request,redirect,make_response

application = Flask(__name__)
host="localhost:8080"

def user(x):    #ログインuser情報を取得する関数
    #mysqlに接続する
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()
    sql = 'SELECT * FROM users WHERE name = %s'
    con.execute(sql,[x])
    info =con.fetchone()
    db.close()      #mysqlの切断
    con.close()
    return info #returnでinfoを返すことができる

@application.route('/')
def trymyself():
    return render_template('login.html')

@application.route('/login')
def index2():
    return render_template('login.html')

@application.route('/login', methods=['POST'])
def login_suru():
    login_G = request.form['login_ID']
    Pass_G = request.form['Password']

    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()
    userinfo=user(login_G)
    if userinfo[3] == Pass_G:  #照合に合格した時の処理
      html = make_response(redirect('http://' + host + '/top'))
      max_age = 60 * 60 * 24 * 120 # 120 days
      expires = int(datetime.now().timestamp()) #+ max_age
      html.set_cookie('username', userinfo[2],expires)    #cookieをset users_name

    else:   #照合に失敗した場合の処理を記入する
      html = render_template('login.html')
    #DBの切断
    db.close()
    con.close()
    return html

@application.route('/top')
def index3():
    data = request.cookies.get('username', None)
    if data is None:    #cookieの情報確認
      html = render_template('login.html')
    else:
      list=[]   #ツイートを格納する配列
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()
      userinfo = user(data)

      sql = 'SELECT follow_you FROM follow WHERE follow.delete_flg=0 and follow_me = %s'
      con.execute(sql,[userinfo[0]])
      result = con.fetchall()
      test2 = result    #userがフォローしている人達のid

      for row in test2: #フォローしている人のツイートを取得
          sql = ('SELECT * from users ' +
                 'inner join tweetInfo on tweetInfo.users_id = users.id ' +
                 'WHERE users_id = %s')
          con.execute(sql,[row[0]]) #各ユーザのツイート
          test3 = con.fetchall()
          for row in test3: #ツイート情報を個別に配列する
              sql = 'SELECT * from favorite WHERE tweet_id = %s and user_id = %s'
              con.execute(sql,[row[7],userinfo[0]]) #row[7]=tweet_id,userinfo=ログインuser_id
              favorite = con.fetchall()
              if favorite is ():
                  #print('お気に入りじゃない')
                  newrow=row + (0,1)
              else:
                  #print('お気に入り')
                  newrow=row + (1,1)
              list.append(newrow)

      html = render_template('index.html', id=userinfo[0],name=data,rows=list)
      #DBの切断
      db.close()
      con.close()
    return html

@application.route('/favorite')
def favarite():
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()
      userinfo = user(data)

      sql = 'select * from favorite where user_id = %s and favorite.delete_flg=0'
      con.execute(sql,[userinfo[0]])
      favarite_info = con.fetchall()    #ueserがfavariteしてるtweet_id

      list=[]
      for row in favarite_info: #favariteのtweetを1つずつ処理する
          sql = ('SELECT * from users ' +
                 'inner join tweetInfo on tweetInfo.users_id = users.id ' +
                 'WHERE tweetInfo.id = %s ')

          con.execute(sql,[row[2]])
          tweet_info = con.fetchall()

          sql = 'SELECT * from follow WHERE follow_me = %s and follow_you = %s'
          con.execute(sql,[userinfo[0],tweet_info[0][8]])
          follow = con.fetchall()
          if follow is ():
              #print('フォローしてない')
              newrow=tweet_info[0] + (1,0)
          else:
              #print('フォロー中')
              newrow=tweet_info[0] + (1,1)
          list.append(newrow)
      html = render_template('index.html', id=userinfo[0],name=data,rows=list)
      db.close()
      con.close()
    return html

@application.route('/search')
def search():
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()
      userinfo = user(data)
      sql = ('SELECT * from users ' +
             'inner join tweetInfo on tweetInfo.users_id = users.id ')
      con.execute(sql)
      All_tweet = con.fetchall()
      list=[]
      for row in All_tweet: #ツイート情報を個別に配列する
          sql= ('SELECT * from favorite WHERE favorite.delete_flg=0 and ' +
                '(tweet_id = %s and user_id = %s)')
          con.execute(sql,[row[7],userinfo[0]])
          favorite = con.fetchall()
          if favorite is ():#('お気に入りじゃない')
              newrow=row + (0,)
          else:#('お気に入り')
              newrow=row + (1,)

          sql = ('SELECT * from follow ' +
                 'WHERE follow.delete_flg=0 and '+
                 '(follow.follow_me = %s and follow.follow_you = %s)')
          con.execute(sql,[userinfo[0],row[0]])
          follow = con.fetchall()
          if follow is ():#('フォローしてない')
              newrow2=newrow + (0,)
          else:#('フォロー中')
              newrow2=newrow + (1,)
          list.append(newrow2)

      db.close()  #DBの切断
      con.close()
      html = render_template('search.html',name=data,rows=list)
    return html

@application.route('/follow/<userid>')
def follow(userid=None):#選択したuserのid
    login_user = request.cookies.get('username', None)#ログインuserのname
    userinfo=user(login_user)
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()
    sql = ('SELECT * from follow ' +
           'WHERE follow.delete_flg=0 and (follow.follow_me = %s and follow.follow_you = %s)')
    con.execute(sql,[userinfo[0],userid])
    follow = con.fetchall()
    if follow is ():  #フォローしてない時の処理 insertする
      sql = 'insert into follow(follow_me,follow_you,delete_flg) value (%s,%s,0)'
      con.execute(sql,[userinfo[0],userid])
      db.commit()
    else:               #フォローしてる時の処理  delete_flgをupdateする
      sql = 'update follow set delete_flg=1 where follow.follow_me = %s and follow.follow_you = %s'
      con.execute(sql,[userinfo[0],userid])
      db.commit()
    html = redirect('http://' + host + '/top')#ここでtop　favariteの判断したい
    db.close()
    con.close()
    return html

@application.route('/favorite/<tweetid>')
def favorite(tweetid=None):#選択したtweetのid
    login_user = request.cookies.get('username', None)#ログインuserのname
    userinfo=user(login_user)
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()

    sql = ('SELECT * from favorite ' +
           'WHERE favorite.delete_flg=0 and '+
           '(favorite.user_id = %s and favorite.tweet_id = %s)')
    con.execute(sql,[userinfo[0],tweetid])
    favorite = con.fetchall()
    if favorite is ():  #フォローしてない時の処理 insertする
      sql = 'insert into favorite(user_id,tweet_id,delete_flg) value (%s,%s,0)'
      con.execute(sql,[userinfo[0],tweetid])
      db.commit()
    else:               #フォローしてる時の処理  delete_flgをupdateする
      sql = ('update favorite set delete_flg=1 '+
             'where favorite.user_id = %s and favorite.tweet_id = %s')
      con.execute(sql,[userinfo[0],tweetid])
      db.commit()
    html = redirect('http://' + host + '/top')#ここでtop　favariteの判断したい
    db.close()
    con.close()
    return html

@application.route('/tubuyaita-')
def tubuyaki1():
    return render_template('tweet.html',name=request.cookies.get('username', None))

@application.route('/tubuyaita-', methods=['POST'])
def tubuyaki2():
    tubuyaki = request.form['tweet']  #login_id

    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()
    data = request.cookies.get('username', None)    #cookieからuser名を取得
    userinfo=user(data)
    sql = 'insert into tweetInfo(users_id,tweet) value (%s,%s)' #time_nowも追加必要
    con.execute(sql,[userinfo[0],tubuyaki])
    db.commit()

    db.close()
    con.close()
    return redirect('http://' + host + '/top')


@application.route('/new')
def show_new():#新規追加画面を表示する
    return render_template('registration.html')

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

      sql='SELECT * FROM tukutter_2.users where Login = %s'
      con.execute(sql,[name_n])
      checkname = con.fetchall()
      if checkname is ():  #かぶってない
        sql = 'insert into users(Login,name,pass) value (%s,%s,%s)'
        con.execute(sql,[login_n,name_n,pass_n])
        db.commit()
        html = render_template('login.html')
      else:             #かぶってる
        #pass
        naiyou = '名前が既に使用されてます。変更お願いします。'
        html=render_template('registration_miss.html',info=naiyou)

      #DBの切断
      db.close()
      con.close()
    else:
      naiyou = 'パスワードが一致しません。もう一度入力お願いします。'
      html=render_template('registration_miss.html',info=naiyou)
    return html

@application.route('/logout')
def logout_suru():
    html = make_response(render_template('login.html'))
    expires = 0
    Value = 'None'
    html.set_cookie('username', Value,expires)
    return html

@application.route('/plofile/<username>')
def plofile(username=None):
    data = request.cookies.get('username', None)
    if data is None:    #cookieにuser情報がないときの処理 ログイン画面に飛ばす
      html = render_template('login.html')
    else:   #cookieにuser情報があるときの処理　表示する
      db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
      con = db.cursor()

      login_user=user(data)
      sql = 'SELECT * FROM users WHERE name = %s'
      con.execute(sql,[username])
      select_user =con.fetchone()
      if login_user[2] == select_user[2]:
        hantei = 1
      else:
        hantei = 0
      #user自身のツイートを取得
      #sql = 'select * from tweetInfo where users_id = %s'
      sql = 'SELECT * from users inner join tweetInfo on tweetInfo.users_id = users.id WHERE users_id = %s'
      con.execute(sql,[login_user[0]])
      tweet_info = con.fetchall()

      tweet_list=[]
      for row in tweet_info:
          tweet_list.append(row)
      db.close()
      con.close()
      html = render_template('profile.html', user=login_user,tweets=tweet_list,hantei = hantei)
    return html
