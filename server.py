from flask import Flask, render_template, request, url_for, session, redirect
from flask_bcrypt import Bcrypt
import numpy as np
import database


app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.secret_key = '1929501024501295912850129'
bcrypt = Bcrypt(app)


@app.route('/')
@app.route('/main')
def index():
    if session.get('logFlag') == True:
        return render_template('index.html')
    else:
        session['logFlag'] = False
        return render_template('index.html')


#-----------------------------------------------------------------------------------------------


@app.route('/notice/<page>', methods=['GET', 'POST'])
def notice(page):

    try:
        if request.method == 'GET':
            admin = database.admin()
            noticeboard = admin.select_board(type = 'N')

            board_cnt = int(np.ceil(len(noticeboard) / 10))
            board = list(reversed(noticeboard))

            board = board[int(page) * 10:(int(page) + 1) * 10]
            pagecnt = range(board_cnt)[(int(page) // 10) * 10 : ((int(page) // 10) + 1) * 10]

            return render_template('notice.html', board = board, pagecnt = pagecnt, board_cnt=board_cnt, page=int(page))

        else:
            ret = request.form.get('bt')
        
            if ret == 'write':
                if session['logFlag']:
                    return redirect('/write')
                else:
                    return render_template('login_error.html')
            elif ret == 'all':
                return redirect('/notice/0')

            else:
                admin = database.admin()
                noticeboard = admin.select_board(type = 'N', head=ret)

                board_cnt = int(np.ceil(len(noticeboard) / 10))
                board = list(reversed(noticeboard))

                board = board[int(page) * 10:(int(page) + 1) * 10]
                pagecnt = range(board_cnt)[(int(page) // 10) * 10 : ((int(page) // 10) + 1) * 10]

                return render_template('notice.html', board = board, pagecnt = pagecnt, board_cnt=board_cnt, page=int(page))

    except:
        return render_template('login_error.html')
        
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/board/<page>', methods=['GET', 'POST'])
def board(page):
    if request.method == 'GET':
        try:
            admin = database.admin()
            noticeboard = admin.select_board(type = 'B')

            board_cnt = int(np.ceil(len(noticeboard) / 10))
            board = list(reversed(noticeboard))

            board = board[int(page) * 10:(int(page) + 1) * 10]
            pagecnt = range(board_cnt)[(int(page) // 10) * 10 : ((int(page) // 10) + 1) * 10]

            return render_template('board.html', board = board, pagecnt = pagecnt, board_cnt=board_cnt, page=int(page))
        except:
            print('에러')
            return render_template('error.html')
    else:
        ret = request.form.get('bt')
        
        if ret == 'write':
            if session['logFlag']:
                return redirect('/write')
            else:
                return render_template('login_error.html')
        elif ret == 'all':
            return redirect('/board/0')
        else:
            admin = database.admin()
            noticeboard = admin.select_board(type = 'B', head=ret)

            board_cnt = int(np.ceil(len(noticeboard) / 10))
            board = list(reversed(noticeboard))

            board = board[int(page) * 10:(int(page) + 1) * 10]
            pagecnt = range(board_cnt)[(int(page) // 10) * 10 : ((int(page) // 10) + 1) * 10]

            return render_template('board.html', board = board, pagecnt = pagecnt, board_cnt=board_cnt, page=int(page))



@app.route('/write' , methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html')
    else:
        try:
            admin = database.admin()

            title = request.form['title']
            head = request.form['select_head']
            content = request.form['content']
            print(title)
            if head != '익명':
                admin.write(title, head, content, session['name'], session['user'])
            else:
                admin.write(title, '익명', content, '익명', session['user'])
            return redirect('/board/0')
        except:
            return "error"

@app.route('/delete/<boardid>')
def delete(boardid):
    if session['logFlag']:
        try:
            admin = database.admin()
            content = admin.select_content(boardid)

            if (content['EMAIL'] == session['user']):
                admin.delete(boardid)
                return render_template("delete_check.html")
            else:
                return render_template('login_error.html')
        except:

            return render_template("error.html")
    else:
        return render_template('login_error.html')

@app.route('/edit/<boardid>', methods=['GET', 'POST'])
def edit(boardid):
    if session['logFlag']:
        if request.method == 'GET':
            try:
                admin = database.admin()
                content = admin.select_content(boardid)

                if (content['EMAIL'] == session['user']):
                    return render_template('edit.html', content=content)
            except:
                return render_template('error.html')
        else:
            try:
                admin = database.admin()
                title = request.form['title']
                head = request.form['select_head']
                content = request.form['content']
                
                admin.edit(boardid = boardid, title = title, content=content, head=head)
                
                return redirect('/board/0')
            except:
                return render_template('error.html')
    else:
        return render_template('login_error.html')
    
@app.route('/content/<boardid>', methods=['GET', 'POST'])
def content(boardid):
    try:
        if request.method == 'GET':
            admin = database.admin()
            admin.upviewcnt(boardid)
            content = admin.select_content(boardid)
            return render_template('content.html', content = content)
    
    except:
        return render_template('error.html')


#------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        
        admin = database.admin()
        info = admin.select_info(email)
        
        hs_pass = info['PASSWORD']
        name = info['NAME']
        
        
        if info != None:
            checked = bcrypt.check_password_hash(hs_pass, password)
            try:
                if checked:
                    session['logFlag'] = True
                    session['user'] = email
                    session['name'] = name

                    return redirect('/main')
                else:
                    return redirect('/login')
            except:
                return render_template('error.html')
        else:
            return render_template('login_error.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop("user", None)
    session['logFlag'] = False
    session.pop("name", None)
    return redirect('/main')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':

        return render_template('signup.html')
    else:
        admin = database.admin()

        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        name = request.form['USERNAME']
        major = request.form['MAJOR']
        age = request.form['AGE']
        
        hash_pw = bcrypt.generate_password_hash(password, 10).decode('utf-8')

        try:
            admin.signup(email=email, password=hash_pw, name=name, phone=phone, major=major, age=age)

            return redirect('/login')

        except:
            return redirect('/signup')


@app.route('/profile/<name>')
def profile():

    return render_template("profile_detail.html")


# 메인 테스트
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

#게시판 글쓰기 페이지, 로그인 페이지