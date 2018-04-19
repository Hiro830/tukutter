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
