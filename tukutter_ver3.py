from datetime import  datetime
import MySQLdb
from flask import Flask, render_template,request,redirect,make_response

application = Flask(__name__)
host="localhost:8080"

def Get_tweet(x,L):   #全部のtweetにuser情報を追加し、ログインuserがfollow,favoriteの判定
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()
    userinfo = user(x)

    if L =='login_user':
        sql = ('SELECT * from users ' +
               'inner join tweetInfo on tweetInfo.users_id = users.id ')
        con.execute(sql)
        All_tweet = con.fetchall()
    else:
        sql = ('SELECT * from users ' +
               'inner join tweetInfo on tweetInfo.users_id = users.id where users_id = %s')
        con.execute(sql,[L])
        All_tweet = con.fetchall()

    All_list=[]
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
        All_list.append(newrow2)
    return All_list

def user(x):    #ログインuser情報を取得する関数
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()
    sql = 'SELECT * FROM users WHERE name = %s'
    con.execute(sql,[x])
    info =con.fetchone()
    db.close()
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

@application.route('/top')  #topならpage=0
def index3():
    data = request.cookies.get('username', None)
    if data is None:    #cookieの情報確認
      html = render_template('login.html')
    else:
      list=[]   #ツイートを格納する配列
      Get_list=[]
      userinfo = user(data)
      Get_list=Get_tweet(data,'login_user')

      for follow_search in Get_list:
          if follow_search[13] ==1 :
              list.append(follow_search)
      html = render_template('index.html', id=userinfo[0],name=data,rows=list,page=0)
    return html

@application.route('/favorite') #favoriteならpage=1
def favarite():
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      list=[]   #ツイートを格納する配列
      Get_list=[]
      userinfo = user(data)
      Get_list=Get_tweet(data,'login_user')

      for favorite_search in Get_list:
          if favorite_search[12] ==1 :
              list.append(favorite_search)
      html = render_template('index.html', id=userinfo[0],name=data,rows=list,page=1)
    return html

@application.route('/search')
def search():
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      Get_list=[]
      userinfo = user(data)
      Get_list=Get_tweet(data,'login_user')
      html = render_template('search.html',name=data,rows=Get_list)
    return html

@application.route('/searchget',methods=['get'])
def search_get():
    data = request.cookies.get('username', None)
    if data is None:
      html = render_template('login.html')
    else:
      list=[]   #ツイートを格納する配列
      Get_list=[]
      userinfo = user(data)
      Get_list=Get_tweet(data,'login_user')
      serch_word = request.args.get('search_query')

      for search in Get_list:
          index = search[9].find(serch_word)
          if index != -1 :
              list.append(search)
      html = render_template('search.html',name=data,rows=list)
    return html


def follow_method(select_user):
    login_user = request.cookies.get('username', None)#ログインuserのname
    userinfo=user(login_user)
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()
    sql = ('SELECT * from follow ' +
           'WHERE follow.delete_flg=0 and (follow.follow_me = %s and follow.follow_you = %s)')
    con.execute(sql,[userinfo[0],select_user])
    follow = con.fetchall()
    if follow is ():  #フォローしてない時の処理 insertする
      sql = 'insert into follow(follow_me,follow_you,delete_flg) value (%s,%s,0)'
      con.execute(sql,[userinfo[0],select_user])
      db.commit()
    else:               #フォローしてる時の処理  delete_flgをupdateする
      sql = 'update follow set delete_flg=1 where follow.follow_me = %s and follow.follow_you = %s'
      con.execute(sql,[userinfo[0],select_user])
      db.commit()
    db.close()
    con.close()

#お気に入り＝1,TOP=0
@application.route('/followtop/<userid>')   #TOP
def follow1(userid=None):#選択したuserのid
    follow_method(userid)
    html = redirect('http://' + host + '/top')
    return html

@application.route('/followfavo/<userid>')  #favorite
def follow2(userid=None):#選択したuserのid
    follow_method(userid)
    html = redirect('http://' + host + '/favorite')
    return html

@application.route('/followserch/<userid>')  #favorite
def follow3(userid=None):#選択したuserのid
    follow_method(userid)
    html = redirect('http://' + host + '/search')
    return html


def favorite_method(select_user):#選択したtweetのid
    login_user = request.cookies.get('username', None)#ログインuserのname
    userinfo=user(login_user)
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter_2', charset='utf8')
    con = db.cursor()

    sql = ('SELECT * from favorite ' +
           'WHERE favorite.delete_flg=0 and '+
           '(favorite.user_id = %s and favorite.tweet_id = %s)')
    con.execute(sql,[userinfo[0],select_user])
    favorite = con.fetchall()
    if favorite is ():  #フォローしてない時の処理 insertする
      sql = 'insert into favorite(user_id,tweet_id,delete_flg) value (%s,%s,0)'
      con.execute(sql,[userinfo[0],select_user])
      db.commit()
    else:               #フォローしてる時の処理  delete_flgをupdateする
      sql = ('update favorite set delete_flg=1 '+
             'where favorite.user_id = %s and favorite.tweet_id = %s')
      con.execute(sql,[userinfo[0],select_user])
      db.commit()
    db.close()
    con.close()

#お気に入り＝1,TOP=0
@application.route('/favotop/<userid>')   #TOP
def favo1(userid=None):#選択したuserのid
    favorite_method(userid)
    html = redirect('http://' + host + '/top')
    return html

@application.route('/favofavo/<userid>')  #favorite
def favo2(userid=None):#選択したuserのid
    favorite_method(userid)
    html = redirect('http://' + host + '/favorite')
    return html

@application.route('/favoserch/<userid>')  #favorite
def favo3(userid=None):#選択したuserのid
    favorite_method(userid)
    html = redirect('http://' + host + '/search')
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
      userinfo=user(data)
      sql = 'SELECT * FROM users WHERE name = %s'
      con.execute(sql,[username])
      select_user =con.fetchone()

      if userinfo[2] == select_user[2]:
        user_check = 1
      else:
        user_check = 0

      Get_list=[]
      Get_list=Get_tweet(data,select_user[0])
      #print(Get_list)
      db.close()
      con.close()
      html = render_template('profile.html', user=userinfo, tweets=Get_list, check = user_check)
    return html
