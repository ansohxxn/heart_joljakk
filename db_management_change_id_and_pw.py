#데이터베이스 관리 프로그램 (테이블 생성, 데이터 삽입, 삭제, 검색, 이미지 반환)
import pymysql
import csv
import os
import base64
from random import choice

#테이블 생성하기 (초기화 과정)
def create_table():
    try:
        # db 접속
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb', charset='utf8mb4')

        # 커서 가져오기
        with db.cursor() as cursor:

            # 1. 테이블 2개 생성
            # 1-1. csv 테이블
            sql_csv = '''CREATE TABLE IF NOT EXISTS table_csv (
                               id INT UNSIGNED NOT NULL,
                               title TEXT NOT NULL,
                               poet VARCHAR(10) NOT NULL,
                               tag VARCHAR(10) NOT NULL,
                               PRIMARY KEY(id)
                        );'''
            # 실행
            cursor.execute(sql_csv)

            # 1-2. image 테이블
            sql_image = '''CREATE TABLE IF NOT EXISTS table_image (
                               id_image INT UNSIGNED NOT NULL,
                               image LONGBLOB NOT NULL,
                               FOREIGN KEY(id_image) REFERENCES table_csv(id) ON DELETE CASCADE,
                               PRIMARY KEY(id_image)
                        );'''
            cursor.execute(sql_image)
            print("db에 sql_csv와 sql_image 테이블을 생성하였습니다.")

            # 2. csv를 db에 넣기
            csvdata = csv.reader(open('C:/Users/HYJ/Desktop/database/merged_csv.csv', encoding='utf-8'))
            for record in csvdata:
                print(record)
                cursor.execute('INSERT INTO table_csv(id, title, poet, tag)' 'VALUES(%s, %s, %s, %s)', record)
            db.commit()
            print("poemdb에 csv 파일을 삽입했습니다.")
    finally:
        cursor.close()
        db.close()

    try:
        # 3. image를 db에 넣기
        # 재접속
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb',
                             charset='latin1')  # charset변경

        with db.cursor() as cursor:
            file_path = '/home/pi/dbfiles/dbimage/'  # 디렉토리 경로
            file_list = os.listdir(file_path)                         # 디렉토리 하위 파일 목록

            # 파일 하나씩 db에 삽입
            file_id = 0                                                # id는 0부터 시작 (csv id와 통일)
            for one_file in file_list:
                full_path = file_path + one_file                       # 파일 전체 경로
                with open(full_path, 'rb') as image:                  # image 열기
                    photo_encoded = base64.b64encode(image.read())     # bas64로 인코딩

                sql = """ INSERT INTO table_image
                    (id_image, image) VALUES (%s,%s)"""
                print("{} has inserted".format(one_file))
                sql_tuple = (file_id, photo_encoded)
                #image를 db에 삽입
                cursor.execute(sql, sql_tuple)
                file_id += 1
                db.commit()
            print("\npoemdb에 이미지를 삽입 완료했습니다.")

    finally:
        cursor.close()
        db.close()

# 데이터 삽입하기
def insert_data():
    # 추가할 시 정보 입력받기
    poem_data = input("시의 id, 제목, 시인, 태그를 입력하세요.(쉼표로 구분) >> ")
    poem_data_list = poem_data.split(',')

    #print(poem_data_list)
    poem_data_list[0] = int(poem_data_list[0])                          # index를 정수로 바꿔줌
    poem_data_id = poem_data_list[0]

    # 삽입할 이미지의 경로 사용자로 부터 입력 받기
    img_data = input("이미지 파일 경로를 입력하세요: ")

    try:
        # db 접속
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb', charset='utf8mb4')
        with db.cursor() as cursor:

            # 시추가
            cursor.execute('INSERT INTO table_csv(id, title, poet, tag)' 'VALUES(%s, %s, %s, %s)', poem_data_list)
            db.commit()
            print("csv_poem에 시 id, title, poet, tag를 모두 추가하였습니다.")

    finally:
        cursor.close()
        db.close()

    try:
        # 재접속
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb',
                             charset='latin1')
        with db.cursor() as cursor:
            # 이미지 삽입
            with open(img_data, 'rb') as image:                         # image 인코딩
                photo_encoded = base64.b64encode(image.read())

            sql = """ INSERT INTO table_image
                    (id_image, image) VALUES (%s,%s)"""
            sql_tuple = (poem_data_list[0], photo_encoded)
            cursor.execute(sql, sql_tuple)                               # image를 db에 삽입

            db.commit()
            print("ID {} 에 이미지를 삽입하였습니다.".format(poem_data_id))

    finally:
        cursor.close()
        db.close()


# 이미지 반환 및 검색
def retrieve_img():
    try:
        # 접속
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb',
                             charset='latin1')

        with db.cursor() as cursor:
            # image테이블 접근
            id_image = int(input("검색할 id를 입력하세요: "))
            sql = "SELECT image FROM table_image WHERE id_image = %s"
            sql_tuple = (id_image,)

            cursor.execute(sql, sql_tuple)

            filepath = '/home/pi/dbfiles/new_photo.png'  # 지정경로
            image = cursor.fetchone()[0]
            # print(image)

            # 이미지를 디렉토리-파일에 쓰기
            with open(filepath, 'wb') as f:                                         # base64로 이미지 디코드
                f.write(base64.b64decode(image))

            print("파일에 이미지를 생성하였습니다. 지정경로에서 확인하세요.\n**지정경로: {}".format(filepath))

    finally:
        cursor.close()
        db.close()

# 데이터 삭제
def delete_data():
    try:
        # 접속
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb',
                             charset='utf8mb4')

        # 삭제할 시제목, 시인 입력받아서 확인
        with db.cursor() as cursor:
            title = input("삭제할 [시 제목]을 입력하세요.>> ")
            poet = input("삭제할 [시인]을 입력하세요.>> ")
            print("삭제하는 시 제목은 [" + title + "] 이고 시인은 [" + poet + "]입니다. 맞습니까? (맞으면 [yes] 틀리면 [no]를 입력하세요.)")
            answer = input("yes/no? >>")

            while True:
                # 삭제할 정보를 데이터베이스에서 삭제
                   # 올바른 정보를 입력받은 경우, 삭제
                if answer == 'yes' or answer == 'YES':
                    sql = """DELETE FROM table_csv WHERE title = %s and poet = %s"""
                    cursor.execute(sql, (title, poet,))
                    db.commit()
                    break

                    # 잘못된 정보를 입력받은 경우, 재입력 받음
                elif answer == 'no' or answer == 'NO':
                    print("정보를 다시 입력해주세요.")
                    title = input("삭제할 [시 제목]을 입력하세요.>> ")
                    poet = input("삭제할 [시인]을 입력하세요.>> ")
                    print("삭제하는 시 제목은 [" + title + "] 이고 시인은 [" + poet + "]입니다. 맞습니까? (맞으면 [yes] 틀리면 [no]를 입력하세요.)")
                    answer = input("yes/no? >>")

                # 오타시 재입력 받음
                else:
                    print("yes나 no만 입력가능합니다. 다시 입력해주세요.")

    finally:
        cursor.close()
        db.close()

# 데이터 검색
def find_data():
    print("찾고자 하는 정보를 입력하세요. (id는 1번, 시제목은 2번, 시인은 3번, 종료는 4번)")
    num = input(">> ")
    try:
        # 접속
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb',
                             charset='utf8mb4')
        with db.cursor() as cursor:

            while True:
                # id로 검색하기
                if num == '1':
                    id_num = input("검색할 id를 입력하세요. ex) 50 >>")
                    sql = "SELECT * FROM table_csv WHERE id = {}".format(id_num)
                    cursor.execute(sql)
                    records = cursor.fetchall()

                    for data in records:
                        print("id : {}, 시제목: {}, 시인 : {}, 태그 : {}".format(data[0], data[1], data[2], data[3]))

                    print("찾고자 하는 정보를 입력하세요. (id는 1번, 시제목은 2번, 시인은 3번, 종료는 4번)")
                    num = input(">> ")
                # 시 제목으로 검색하기
                elif num == '2':
                    title_info = input("검색할 시제목을 입력하세요. 띄어쓰기를 주의하세요. ex) 가난한사랑노래 >> ")
                    sql = """SELECT * FROM table_csv WHERE title = %s"""
                    cursor.execute(sql, (title_info,))
                    record = cursor.fetchone()
                    print("id : {}, 시제목: {}, 시인 : {}, 태그 : {}".format(record[0], record[1], record[2], record[3]))

                    print("찾고자 하는 정보를 입력하세요. (id는 1번, 시제목은 2번, 시인은 3번, 종료는 4번)")
                    num = input(">> ")
                # 시인으로 검색하기
                elif num == '3':
                    poet_info = input("검색할 시인을 입력하세요. ex) 정현철 >>")
                    sql = """SELECT * FROM table_csv WHERE poet = %s"""
                    cursor.execute(sql, (poet_info,))
                    record = cursor.fetchall()

                    for data in record:
                        print("id : {}, 시제목: {}, 시인 : {}, 태그 : {}".format(data[0], data[1], data[2], data[3]))

                    print("찾고자 하는 정보를 입력하세요. (id는 1번, 시제목은 2번, 시인은 3번, 종료는 4번)")
                    num = input(">> ")
                # 검색 종료!
                elif num == '4':
                    print("시 정보를 찾기를 종료합니다.")
                    break
                # 오타 입력 받음, 재입력
                else:
                    print("잘못된 숫자를 입력하셨습니다. 1,2,3,4 중에 입력하세요.")
                    num = input(">> ")

    finally:
        cursor.close()
        db.close()

def main():
    create_table()                                       # 초기에만 실행, 이후 '#' 붙일 것

    # 관리 목록..
    while True:
        print("""-------------시 데이터베이스 메뉴------------
1. 시 데이터 추가
2. 시 데이터 삭제
3. 시 데이터 사진 반환
4. 시 검색
5. 종료
""")
        num = int(input("검색할 메뉴를 고르세요.>> "))
        if num == 1:
            insert_data()
        elif num == 2:
            delete_data()
        elif num == 3:
            retrieve_img()
        elif num == 4:
            find_data()
        elif num == 5:
            print("\n데이터베이스 메뉴를 종료합니다.\n")
            break
        else:
            print("잘못된 언어를 입력하셨습니다.\n")


if __name__ == "__main__":
    main()
