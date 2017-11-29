import MySQLdb
from flask import Flask, render_template,request,redirect

application = Flask(__name__)

@application.route('/login', methods=['POST'])
def login():
    task = request.form['login_ID']

    #mysqlに接続する
    db = MySQLdb.connect( user='root', passwd='A12qwerzxcv123', host='localhost', db='tukutter', charset='utf8')
    con = db.cursor()

    #passを取得する
    sql = 'SELECT pass FROM users WHERE Login = %s'
    con.execute(sql,[task])
    result = con.fetchall()
    print (result)
    #DBの切断
    db.close()
    con.close()

    task = result[0][0]
    print (task)





    return task
