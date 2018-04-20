def follow_method(user,select_user):
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

##上の関数に以下をあてはめて戻ってくるようにする
@application.route('/followtop/<userid>')
def follow(userid=None):#選択したuserのid
    page='top'
    return html

@application.route('/followfavo/<userid>')
def follow(userid=None):#選択したuserのid
    page='favorite'
    return html
