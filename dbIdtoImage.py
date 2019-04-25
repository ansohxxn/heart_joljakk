# 챗봇에서 받은 태그에 따른 시를 이미지로 반환하는 프로그램
  # 과정: 1. 태그에 해당하는 id 리스트를 얻음
  #       2. id 중 랜덤으로 하나만 추출
  #       3. 해당 이미지 검색하여 디렉토리에 저장

import pymysql
import base64
from random import choice

# 태그에 맞는 이미지 반환
def tag_to_id(tag):

    try:
        # 접속
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb',
                             charset='utf8mb4')

        with db.cursor() as cursor:
            sql = """SELECT * FROM table_csv WHERE tag = %s"""
            count_tag = cursor.execute(sql, (tag,))      #tag의 개수를 알려줌
            record = cursor.fetchall()                   #((id, title, poet, tag)) 형식으로 출력

            id_list = []
            for data in record:
                id_list.append(data[0])
                # (아래) 전체 정보 확인용
                #print("id : {}, 시제목: {}, 시인 : {}, 태그 : {}".format(data[0], data[1], data[2], data[3]))

        random_id = choice(id_list)                      #랜덤으로 tag에 해당하는 id 중 하나 추출
        #print(id_list)
        #print(random_id)

        #뽑힌 id의 이미지를 반환 (charset이 다르므로 db에 재접속해야 함)
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb',
                             charset='latin1')            # charset변경

        with db.cursor() as cursor:
            # image테이블 접근
            sql = "SELECT image FROM table_image WHERE id_image = %s"
            sql_tuple = (random_id,)

            cursor.execute(sql, sql_tuple)

            filepath = '/home/pi/dbfiles/new_photo.png'  # 지정경로
            image = cursor.fetchone()[0]

            # 이미지를 디렉토리-파일에 쓰기
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(image))

            print("파일에 이미지를 생성하였습니다. 지정경로에서 확인하세요.\n**지정경로: {}".format(filepath))

    finally:
        cursor.close()
        db.close()
        return random_id

def getTitle(idnum):
    try:
        # 접속
        db = pymysql.connect(host='localhost', user='joljak', passwd='joljakplz', db='poemdb',
                             charset='utf8mb4')


        with db.cursor() as cursor:
            sql = """SELECT title FROM table_csv WHERE id = %s"""
            cursor.execute(sql, (idnum,))  # tag의 개수를 알려줌
            title = cursor.fetchone()[0]  # (title,) 형식으로 출력

    finally:
        cursor.close()
        db.close()
        return title


def getPoet(idnum):
    try:
        # 접속
        db = pymysql.connect(host='localhost', user='root', passwd='joljakk', db='poemdb',
                             charset='utf8mb4')

        with db.cursor() as cursor:
            sql = """SELECT poet FROM table_csv WHERE id = %s"""
            cursor.execute(sql, (idnum,))  # tag의 개수를 알려줌
            poet = cursor.fetchone()[0]  # (poet,) 형식으로 출력

    finally:
        cursor.close()
        db.close()
        return poet

def main():
    tag_ = '사랑'                         #테스트
    id = tag_to_id(tag_)
    #print(id)
    title = getTitle(id)
    #print(title)
    poet = getPoet(id)
    #print(poet)

if __name__ == '__main__':
    main()

