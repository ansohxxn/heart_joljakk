import pymysql

try:
    # db 접속
    db = pymysql.connect(host='localhost', user='root', passwd='joljakk', db='poemdb', charset='utf8mb4')

    with db.cursor() as cursor:
        sql = """select host from mysql.user where user='joljak'"""
        cursor.execute(sql)
        users = cursor.fetchall()
        for i in users:
            print(i)

        sql1 = """insert into user(host,user,password,ssl_cipher,x509_issuer,x509_subject)
        values('192.168.47.232','joljak',password('joljak'),'','','')"""
        cursor.execute(sql1)
        sql2 = """grant all privileges on poemdb. * to 'joljak' @ '192.168.47.232'"""
        cursor.execute(sql2)
        sql3 = """flush privileges"""




finally:
    cursor.close()
    db.close()

