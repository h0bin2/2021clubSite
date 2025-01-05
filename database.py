import pymysql

class admin:
    def __init__(self):
        self.db = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="club", charset='utf8')
        self.curs = self.db.cursor(pymysql.cursors.DictCursor)


    def signup(self, email, password, phone, name, major, age):
        sql = f"""INSERT INTO SIGN (EMAIL, PASSWORD, PHONE, NAME, MAJOR, AGE)
        VALUES ('{email}', '{password}', '{phone}','{name}','{major}','{age}')"""

        self.curs.execute(sql)
        self.db.commit()
    
    def select_info(self, email):
        sql = f"SELECT * FROM SIGN WHERE EMAIL = '{email}'"
        self.curs.execute(sql)
        
        info = self.curs.fetchall()[0]
        return info
    
    def select_board(self, type, head=None):
        if head == None:
            sql = f"SELECT *, DATE(REGDATE) FROM BOARD WHERE TYPE = '{type}'"
        else:
            sql = f"SELECT *, DATE(REGDATE) FROM BOARD WHERE TYPE = '{type}' AND HEAD = '{head}'"

        self.curs.execute(sql)
        allboard = self.curs.fetchall()

        return allboard

    def write(self, title, head, content, name, email):
        try:
            maxcnt = self.max_cnt_board()
        except:
            maxcnt = 0

        if head in ('자유', '질문', '익명'):
            type = 'B'
            sql = f"""INSERT INTO BOARD(BOARDID, TITLE, EMAIL, NAME, CONTENTS, TYPE, HEAD)
            VALUES('{maxcnt}', '{title}', '{email}', '{name}', '{content}', '{type}', '{head}')
            """

            self.curs.execute(sql)
            self.db.commit()
			
        elif head in ('공지', '일정'):
            type = 'N'
            sql = f"""INSERT INTO BOARD(BOARDID, TITLE, EMAIL, NAME, CONTENTS, TYPE, HEAD)
            VALUES('{maxcnt}', '{title}', '{email}', '{name}', '{content}', '{type}', '{head}')
            """

            self.curs.execute(sql)
            self.db.commit()

    def delete(self, boardid):
        sql = f"DELETE FROM BOARD WHERE BOARDID = '{boardid}'"
        self.curs.execute(sql)
        self.db.commit()
        
        
    def max_cnt_board(self):
        sql = f'SELECT max(BOARDID) FROM BOARD'
        self.curs.execute(sql)
        max_cnt = self.curs.fetchall()[0]['max(BOARDID)'] + 1

        return max_cnt 

    def select_content(self, boardid):
        sql = f'SELECT * FROM BOARD WHERE BOARDID = "{boardid}"'
        self.curs.execute(sql)

        content = self.curs.fetchall()[0]

        return content
    
    def edit(self, boardid, title, content, head):
        boardid = int(boardid)
        sql = f"UPDATE BOARD SET BOARDID = '{boardid}', TITLE = '{title}', CONTENTS = '{content}', HEAD = '{head}' WHERE BOARDID = {boardid}"
        
        self.curs.execute(sql)
        self.db.commit()
    
    def upviewcnt(self, boardid):
        boardid = int(boardid)
        sql = f'UPDATE BOARD SET VIEWCNT = VIEWCNT + {1} WHERE BOARDID = {boardid}'
        
        self.curs.execute(sql)
        self.db.commit()
        